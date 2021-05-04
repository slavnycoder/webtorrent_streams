from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from common.utils.captcha import validate_captcha


class CaptchaAuthTokenSerializer(AuthTokenSerializer):
    captcha = serializers.CharField(validators=[validate_captcha])


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CaptchaAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
