import imghdr
import io

from django.db import transaction
from django.db.models import Max
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.models import StorageObject
from common.utils import random_string, PNGUploadParser
from file_storages.google_cloud import gs_client
from file_storages.google_cloud.utils import gs_panel_images_path
from users.models import ChannelPanel, User
from users.serializers import ChannelPanelSerializer


class ChannelPanels(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChannelPanelSerializer
    parser_classes = [JSONParser, PNGUploadParser, ]

    def get_queryset(self):
        return ChannelPanel.objects.all()

    def create(self, request, *args, **kwargs):
        channel: User = request.user
        request.data.update({
            "channel": channel.id,
            "sort": ChannelPanel.objects.filter(channel=channel).aggregate(sort=Max("sort") + 1)["sort"] or 0
        })
        return super().create(request, *args, **kwargs)

    @action(["post", "delete", ], detail=True)
    def image(self, request, *args, **kwargs):
        panel: ChannelPanel = self.get_object()
        if request.method == "POST":
            if request.FILES["file"].size > 10 ** 6:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"file": "file is too big"})
            with transaction.atomic():
                filename = f"{random_string(length=20)}.png"
                dest_path = gs_panel_images_path(filename)
                with io.BytesIO(request.FILES["file"].read()) as panel_image:
                    if imghdr.what(panel_image) != "png":
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={"file": "not png"})
                    gs_client.upload_file(panel_image, dest_path)
                if panel.image:
                    panel.image.delete()
                new_image = StorageObject.objects.create(blob_path=dest_path)
                panel.image = new_image
                panel.save()
            return Response(status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            if panel.image:
                panel.image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance: ChannelPanel):
        if instance.channel == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied({"message": "You don't have permission to delete this panel"})
