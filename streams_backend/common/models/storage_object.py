import os

from django.db import models

from common.models import UUIDModel
from file_storages.google_cloud import gs_client


class StorageObject(UUIDModel):
    blob_path = models.CharField(max_length=255)

    @property
    def file_url(self):
        return os.path.join(gs_client.root_path, self.blob_path)

    def delete(self, *args, **kwargs):
        gs_client.delete_file(self.blob_path)
        super().delete(*args, **kwargs)
