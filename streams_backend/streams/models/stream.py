import io
import json
import os
from typing import Optional, List

from django.db import models
from django.utils import timezone

from common.models import UUIDModel
from common.utils import PlaylistGenerator
from file_storages.google_cloud import gs_client, gs_playlist_path, gs_thumbnail_path, gs_playlist_path_json
from streams.models import Chunk
from users.models import User
from websockets import cent_client
from websockets.constants import STREAM_STARTED

TORRENT_STREAM_THRESHOLD = 15


class Stream(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streams')
    description = models.CharField(max_length=255, default='Введите описание стрима')
    live_at = models.DateTimeField(default=timezone.now)

    is_started = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    dttm_last_chunk = models.DateTimeField(default=timezone.now)

    viewers = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        gs_client.delete_folder(f"streams/{self.id}")
        super().delete(*args, **kwargs)

    def generate_playlist(self, chunks_number: int = 3) -> Optional[str]:
        assert chunks_number > 0
        chunks: List["Chunk"] = list(self.chunks.order_by("-number")[:chunks_number])
        if chunks:
            playlist_entries = [
                {
                    "path": chunk.magnet_link if self.viewers > TORRENT_STREAM_THRESHOLD else chunk.torrent_url,
                    "duration": chunk.duration,
                } for chunk in reversed(chunks)
            ]
            return PlaylistGenerator(playlist_entries=playlist_entries, sequence=chunks[-1].number).generate()
        else:
            return None

    @property
    def playlist_url(self):
        return os.path.join(gs_client.root_path, gs_playlist_path(str(self.id)))

    @property
    def playlist_json_url(self):
        return os.path.join(gs_client.root_path, gs_playlist_path_json(str(self.id)))

    @property
    def thumbnail_url(self):
        return os.path.join(gs_client.root_path, gs_thumbnail_path(str(self.id)))

    def ws_notify_start(self):
        from streams.serializers import StreamSerializer

        cent_client.publish(f"channel:{self.user.username}", {
            "type": STREAM_STARTED,
            "stream": StreamSerializer(self).data,
        })

    def update_playlist(self):
        from streams.serializers.chunk import ChunkSerializer

        chunks = Chunk.objects.filter(stream=self, is_public=True).order_by("-number")[:3]
        with io.StringIO(json.dumps(ChunkSerializer(chunks, many=True).data)) as playlist_file:
            new_playlist = gs_client.upload_file(
                playlist_file, gs_playlist_path_json(self.id, new=True), content_type="application/json"
            )
            new_playlist.cache_control = "no-cache, no-store"
            new_playlist.update()
            gs_client.rewrite(new_playlist, gs_playlist_path_json(self.id))

        just_started = False  # TODO add field tracker
        if not self.is_started:
            self.is_started = self.is_live = just_started = True
        self.dttm_last_chunk = max(self.dttm_last_chunk, timezone.now())
        self.save(update_fields=["is_started", "is_live", "dttm_last_chunk", ])

        if just_started:
            self.ws_notify_start()
