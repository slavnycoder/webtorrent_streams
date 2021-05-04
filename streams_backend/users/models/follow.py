from django.db import models

from common.models import UUIDModel
from users.models import User


class Follow(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    channel = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    dttm_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "channel")
