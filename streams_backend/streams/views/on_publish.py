from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from streams.models import Stream
from users.models import User


@csrf_exempt
@require_POST
def on_publish_view(request: HttpRequest):
    stream_key = request.POST['name']
    user = get_object_or_404(User, stream_key=stream_key)
    if not user.is_streamer:
        return HttpResponseForbidden("user is not a streamer")

    with transaction.atomic():
        # TODO allow to continue stream, refactor stream start and new chunk handling in observer
        User.objects.filter(id=user.id).update(stream=None)
        Stream.objects.filter(user=user).update(is_live=False)
        stream = Stream.objects.create(user=user, description=user.stream_description)
    return HttpResponseRedirect(str(stream.id))
