import os
import random
import re
import string
from typing import Optional

from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from common.models import UUIDModel
from file_storages.google_cloud import gs_client
from file_storages.google_cloud.utils import gs_profile_pics_path
from users.constants import USERNAME_COLORS
from websockets import create_ws_token


def get_random_color():
    return random.choice(USERNAME_COLORS)


def generate_stream_key(length: int = 30):
    letters_and_digits = string.ascii_letters + string.digits
    rand_str = ''.join(random.choice(letters_and_digits) for _ in range(length))
    return f'key_{rand_str}'


def validate_username(username):
    if len(username) < 5:
        raise ValidationError(detail={'username': _("min 5 chars")})
    if len(username) > 16:
        raise ValidationError(detail={'username': _("max 16 chars")})
    if not re.match(r"^[a-z0-9_]+$", username):
        raise ValidationError(detail={'username': _("only [a-z] and '_'")})
    if re.match(r"(_)\1", username):
        raise ValidationError(detail={'username': _("no double '_'")})


class User(DjangoAbstractUser, UUIDModel):
    username = models.CharField(
        max_length=16,
        unique=True,
        validators=[validate_username],
        error_messages={
            'unique': 'unique_err',
        },
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'unique_err',
        },
    )
    username_color = models.CharField(max_length=255, default=get_random_color)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    followed = models.ManyToManyField('User', related_name='followers', through="users.Follow", blank=True)

    is_streamer = models.BooleanField(default=False)
    stream_key = models.CharField(max_length=255, default=generate_stream_key)
    stream_description = models.CharField(max_length=255, default='My first stream')
    stream = models.ForeignKey('streams.Stream', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    userpic_filename = models.CharField(max_length=255, null=True, blank=True)

    is_followed: Optional[bool] = None
    followers_count: Optional[int] = None

    def save(self, *args, **kwargs):
        if self.stream_key is None:
            self.stream_key = generate_stream_key()
        super().save(*args, **kwargs)

    @property
    def ws_token(self):
        return create_ws_token(self.username)

    @property
    def userpic_url(self):
        if self.userpic_filename:
            return os.path.join(gs_client.root_path, gs_profile_pics_path(self.userpic_filename))
        else:
            return None

    @property
    def ws_channel(self):
        return f"channel:{self.username}"

    @property
    def ws_chat_channel(self):
        return f"chat:{self.username}"
