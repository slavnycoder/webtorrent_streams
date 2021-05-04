import logging
import os

from django.db import models, transaction
from django.utils import timezone

from backend import settings
from common.models import UUIDModel
from file_storages.google_cloud import gs_client, gs_chunk_path, gs_torrent_path
from websockets import cent_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


class Chunk(UUIDModel):
    stream = models.ForeignKey("streams.Stream", on_delete=models.CASCADE, related_name='chunks')
    number = models.IntegerField()
    filename = models.CharField(max_length=255)
    magnet_link = models.TextField(null=True, blank=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_public = models.BooleanField(default=False)
    prob = models.DecimalField(max_digits=5, decimal_places=4, default=1)
    dttm_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('stream', 'number')

    def __str__(self) -> str:
        return f'{str(self.stream_id)[0:5]} {self.filename}'

    def delete(self, *args, **kwargs):
        gs_client.delete_file(gs_chunk_path(self.stream_id, self.filename))
        super().delete(*args, **kwargs)

    @property
    def file_url(self) -> str:
        return os.path.join(gs_client.root_path, gs_chunk_path(self.stream_id, self.filename))

    @property
    def torrent_path(self) -> str:
        return f"torrents/{self.number}.torrent"

    @property
    def torrent_url(self) -> str:
        return os.path.join(gs_client.root_path, gs_torrent_path(self.stream_id, self.number))

    @transaction.atomic
    def make_private(self):
        gs_client.make_private(gs_chunk_path(self.stream_id, self.filename))
        self.is_public = False
        self.save()

    @transaction.atomic
    def make_public(self):
        gs_client.make_public(gs_chunk_path(self.stream_id, self.filename))
        self.is_public = True
        self.save()

    def ws_broadcast(self):
        cent_client.publish(f"chunks:{settings.CHUNKS_CHANNEL}", {
            "torrent_url": self.torrent_url
        })
