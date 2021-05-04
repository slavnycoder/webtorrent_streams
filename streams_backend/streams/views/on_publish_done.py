from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from streams.models import Stream
from users.models import User


@csrf_exempt
@require_POST
def on_publish_done_view(request: HttpRequest):
    with transaction.atomic():
        stream_key = request.POST['name']
        user = get_object_or_404(User, stream_key=stream_key)
        Stream.objects.filter(user=user, is_live=True).update(is_live=False)
        user.stream = None
        user.save()
        return HttpResponse("OK")
