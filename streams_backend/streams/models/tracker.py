from django.db import models

from common.models import UUIDModel


class Tracker(UUIDModel):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
