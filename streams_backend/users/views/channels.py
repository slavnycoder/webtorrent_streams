from typing import Optional

from django.db.models import F, Count
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.utils.clear_text import clean_text
from users.models import User, Follow
from users.serializers import ChannelSerializer, RetrieveChannelSerializer
from websockets import cent_client
from websockets.constants import CHANNEL_UPDATED, USER_MESSAGE

DEFAULT_ONLINE_PAGE_SIZE = 19


class ChannelsViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    permission_classes = [AllowAny, ]
    serializer_class = ChannelSerializer
    lookup_field = "username"

    def get_queryset(self):
        return User.objects.filter(is_streamer=True).all()

    def list(self, request, *args, **kwargs):
        user: Optional[User] = request.user
        followed_qs = User.objects.none()
        online_qs = self.get_queryset().filter(stream__is_live=True).order_by('-stream__viewers')
        top_qs = self.get_queryset() \
            .annotate(followers_count=Count("followers")) \
            .filter(followers_count__gt=0) \
            .order_by("-followers_count")

        if user and user.is_authenticated:
            followed_qs = user.followed.order_by(F('stream__viewers').desc(nulls_last=True))
            online_qs = online_qs.exclude(id__in=user.followed.values('id'))

        followed_qs = ChannelSerializer.setup_eager_loading(followed_qs)
        online_qs = ChannelSerializer.setup_eager_loading(online_qs)
        top_qs = ChannelSerializer.setup_eager_loading(top_qs)
        return Response({
            "followed": ChannelSerializer(followed_qs, many=True, context=dict(is_followed=True)).data,
            "online": ChannelSerializer(online_qs, many=True, context=dict(is_followed=False)).data,
            "top": ChannelSerializer(top_qs, many=True, context=dict(is_followed=False)).data
        })

    @action(detail=False, methods=["get", ])
    def online(self, *args, **kwargs):
        online_qs = self.get_queryset().filter(stream__is_live=True).order_by("-stream__viewers")
        user: Optional[User] = self.request.user
        if user and user.is_authenticated:
            online_qs = ChannelSerializer.annotate_is_followed(online_qs, user)
        online_qs = online_qs.order_by(F("stream__viewers").desc(nulls_last=True))
        online_qs = ChannelSerializer.setup_eager_loading(online_qs)
        page = max(int(self.request.query_params.get("page", 1)), 1)
        limit = page * DEFAULT_ONLINE_PAGE_SIZE
        return Response({
            "next_page": online_qs[limit:].exists(),
            "channels": ChannelSerializer(online_qs[:limit], many=True).data
        })

    def retrieve(self, request, *args, **kwargs):
        instance_qs = self.get_queryset().filter(username=kwargs["username"])
        instance_qs.prefetch_related("panels__image")
        user: Optional[User] = request.user
        if user and user.is_authenticated:
            instance_qs = RetrieveChannelSerializer.annotate_is_followed(instance_qs, user)
        instance = get_object_or_404(instance_qs)
        serializer = RetrieveChannelSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post", ])
    def follow(self, *args, **kwargs):
        user: User = self.request.user
        if user and user.is_authenticated:
            to_follow = bool(self.request.data.get("to_follow"))
            channel: User = self.get_object()
            followed = deleted = False
            if to_follow:
                _, followed = Follow.objects.get_or_create(user=user, channel=channel)
            else:
                deleted = bool(Follow.objects.filter(user=user, channel=channel).delete()[0])
            if followed or deleted:
                is_followed = followed or not deleted
                cent_client.publish(f"channel:{channel.id}", {
                    "type": CHANNEL_UPDATED,
                    "channel": ChannelSerializer(channel, context=dict(is_followed=is_followed)).data,
                })
            return Response()
        raise PermissionDenied()

    @action(detail=True, methods=['post', ])
    def post_message(self, request, *args, **kwargs):
        user: User = request.user
        if user and user.is_authenticated:
            text = clean_text(request.data.get("text", ""))
            if len(text) > 500:
                raise ValidationError("too_long")
            if not text:
                raise ValidationError("no_text")
            channel: User = self.get_object()
            cent_client.publish(channel.ws_chat_channel, {
                "type": USER_MESSAGE,
                "username": user.display_name or user.username,
                "username_color": user.username_color,
                "text": text,
            })
            return Response()
        raise PermissionDenied()
