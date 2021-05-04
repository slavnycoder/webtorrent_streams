from django.db.models import QuerySet, OuterRef, Exists
from rest_framework import serializers

from streams.serializers import StreamSerializer
from users.models import User, Follow
from users.serializers import ChannelPanelSerializer


class ChannelSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    stream = StreamSerializer()
    img_url = serializers.CharField(source="userpic_url")
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username", "username_color", "display_name", "img_url",
            "stream", "is_followed", "ws_channel", "ws_chat_channel",
            "followers_count",
        ]

    @staticmethod
    def setup_eager_loading(queryset: QuerySet):
        return queryset.select_related('stream')

    @staticmethod
    def annotate_is_followed(queryset: QuerySet, user: User):
        return queryset.annotate(is_followed=Exists(Follow.objects.filter(user=user, channel_id=OuterRef("pk"))))

    def get_display_name(self, obj: User):
        return obj.display_name or obj.username

    def get_is_followed(self, obj: User):
        return bool(obj.is_followed) or bool(self.context.get("is_followed"))


class RetrieveChannelSerializer(ChannelSerializer):
    panels = ChannelPanelSerializer(many=True)

    class Meta(ChannelSerializer.Meta):
        fields = ChannelSerializer.Meta.fields + ["panels", ]
