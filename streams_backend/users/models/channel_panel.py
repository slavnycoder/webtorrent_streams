from django.db import models

from common.models import UUIDModel, StorageObject
from users.models import User


class ChannelPanel(UUIDModel):
    channel = models.ForeignKey(User, on_delete=models.CASCADE, related_name="panels")
    sort = models.IntegerField()

    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ForeignKey(StorageObject, on_delete=models.SET_NULL, null=True, blank=True)
    image_link = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
