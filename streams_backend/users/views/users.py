import imghdr
import io

from django.db import transaction
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from common.utils import random_string, PNGUploadParser
from common.utils.captcha import validate_captcha
from common.utils.clear_text import clean_text
from file_storages.google_cloud.utils import gs_client, gs_profile_pics_path
from streams.models import Stream
from users.models import User


class UserViewSet(DjoserUserViewSet):
    parser_classes = (JSONParser, PNGUploadParser)

    def create(self, request, *args, **kwargs):
        captcha = request.data.pop("captcha")
        validate_captcha(captcha)
        return super().create(request, *args, **kwargs)

    @action(["post", "delete", ], detail=False)
    def userpic(self, request, *args, **kwargs):
        user: User = request.user
        if request.method == "POST":
            if request.FILES["file"].size > 10 ** 5:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"file": "file is too big"})
            with transaction.atomic():
                filename = f"{random_string(length=20)}.png"
                with io.BytesIO(request.FILES["file"].read()) as userpic:
                    if imghdr.what(userpic) != "png":
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={"file": "not png"})
                    gs_client.upload_file(userpic, gs_profile_pics_path(filename))
                if user.userpic_filename:
                    gs_client.delete_file(gs_profile_pics_path(user.userpic_filename))
                user.userpic_filename = filename
                user.save()

            return Response()
        elif request.method == "DELETE":
            if user.userpic_filename:
                with transaction.atomic():
                    gs_client.delete_file(gs_profile_pics_path(user.userpic_filename))
                    user.userpic_filename = None
                    user.save()
            return Response({"deleted": True})
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(["post", ], detail=False)
    def display_name(self, request, *args, **kwargs):
        user: User = request.user
        new_display_name = request.data.get("display_name", None)
        if not new_display_name:
            user.display_name = None
            user.save()
            return Response()
        elif new_display_name.lower() == user.username.lower():
            user.display_name = new_display_name
            user.save()
            return Response()
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(["get", ], detail=False)
    def stream_settings(self, request, *args, **kwargs):
        user: User = request.user
        if user.is_streamer:
            return Response({
                "stream_description": user.stream_description,
                "stream_key": user.stream_key
            })
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(["post", ], detail=False)
    def stream_description(self, request, *args, **kwargs):
        user: User = request.user
        if user.is_streamer:
            new_description = clean_text(request.data.get("stream_description", ""))
            if new_description and len(new_description) <= 80:
                with transaction.atomic():
                    user.stream_description = new_description
                    user.save()
                    Stream.objects.filter(id=user.stream_id, is_live=True).update(description=new_description)
            return Response()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(["post", ], detail=False)
    def reset_stream_key(self, request, *args, **kwargs):
        user: User = request.user
        if user.is_streamer:
            user.stream_key = None
            user.save()
            return Response({"stream_key": user.stream_key})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
