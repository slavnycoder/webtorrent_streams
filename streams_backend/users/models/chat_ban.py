from django.db import models

from common.models import UUIDModel
from users.models import User


class ChatBan(UUIDModel):
    streamer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banned_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bans')
    expires = models.DateTimeField()

    class Meta:
        unique_together = ('streamer', 'user')
