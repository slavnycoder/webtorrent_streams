from djoser.serializers import UserCreateSerializer
from knox.models import AuthToken
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "is_active", "ws_token", "userpic_url", "display_name", "is_streamer",)


class CreateUserSerializer(UserCreateSerializer):
    token = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ('token',)

    def get_token(self, obj: User):
        _, token = AuthToken.objects.create(obj, None)
        return token
