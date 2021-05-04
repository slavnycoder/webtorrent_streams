from datetime import timedelta
from typing import List

from constance import config
from django.utils import timezone

from backend.celery import app
from streams.models import Stream, Chunk
from users.models import User
from websockets import cent_client
from websockets.utils import presence_stats

OLD_CHUNK_THRESHOLD = timedelta(seconds=config.OLD_CHUNK_THRESHOLD)
END_STREAM_AFTER = timedelta(seconds=config.END_STREAM_AFTER)


@app.task
def update_viewers_count(*args, **kwargs):
    streams = []
    online_channels: List[User] = User.objects.filter(is_streamer=True).filter(stream__is_live=True).select_related("stream").all()
    for channel in online_channels:
        stream_obj: Stream = channel.stream
        stream_obj.viewers = presence_stats(cent_client, channel.ws_channel)["result"]["num_users"]
        streams.append(stream_obj)
    Stream.objects.bulk_update(streams, fields=["viewers", ])


@app.task
def clear_old_chunks(*args, **kwargs):
    time_threshold = timezone.now() - OLD_CHUNK_THRESHOLD
    chunks_to_delete = Chunk.objects.filter(dttm_created__lt=time_threshold)[:30]
    if not config.DELETE_OLD_USERS_CHUNKS:
        chunks_to_delete = chunks_to_delete.filter(stream__user__is_staff=True)
    for chunk in chunks_to_delete:
        chunk.delete()


@app.task
def end_outdated_streams(*args, **kwargs):
    Stream.objects.filter(is_live=True, dttm_last_chunk__lt=timezone.now() - END_STREAM_AFTER).update(is_live=False)
