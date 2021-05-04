import hashlib

from rest_framework import response, permissions
from rest_framework.decorators import api_view, permission_classes

from users.models import User
from websockets import create_ws_token


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def ws_settings(request):
    user: User = request.user
    if user and user.is_authenticated:
        ws_token = user.ws_token
    else:
        hasher = hashlib.md5()
        hasher.update(str(request.META.get('REMOTE_ADDR', "no-ip") + "unauth_salt").encode("utf-8"))
        ws_token = create_ws_token(hasher.hexdigest())
    return response.Response({
        "ws_token": ws_token,
    })
