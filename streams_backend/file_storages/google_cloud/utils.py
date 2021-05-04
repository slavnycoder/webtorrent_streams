import json
import os
from typing import Union, Optional, List

from google.cloud import storage
from google.cloud.storage import Blob, Bucket
from google.oauth2.service_account import Credentials

PROJECT_ID = "streams"
BUCKET_NAME = "streams"
PROFILE_PICS_FOLDER = "profile_pics"
PANEL_IMAGES_FOLDER = "panel_images"
STREAMS_FOLDER = "streams"
STATIC_FOLDER = "static"


class GoogleCloudClient:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        credentials = Credentials.from_service_account_info(json.loads(os.environ["GOOGLE_CREDENTIALS"]))
        self.client = storage.Client(project=PROJECT_ID, credentials=credentials)
        self.root_path = f"https://storage.googleapis.com/{bucket_name}/"

    def get_bucket(self) -> Bucket:
        return self.client.get_bucket(self.bucket_name)

    def upload_file(self, source: str, dest_path: str, public: bool = True, content_type: Optional[str] = None) -> Blob:
        dest_blob = self.get_bucket().blob(dest_path)
        if isinstance(source, str):
            dest_blob.upload_from_filename(source, content_type=content_type)
        else:
            dest_blob.upload_from_file(source, rewind=True, content_type=content_type)
        if public:
            dest_blob.make_public()
        return dest_blob

    def rewrite(self, source: Union[Blob, str], dest: Union[Blob, str]):
        if isinstance(dest, str):
            dest = self.get_bucket().blob(dest)
        if isinstance(source, str):
            source = self.get_bucket().blob(source)
        dest.rewrite(source)
        return dest

    def delete_file(self, dest_path: str):
        blob = self.get_bucket().blob(dest_path)
        if blob.exists():
            blob.delete()

    def delete_folder(self, dest_folder: str):
        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]

        blobs: List[Blob] = list(self.get_bucket().list_blobs(prefix=dest_folder))
        blob_batches = chunks(blobs, 999)
        for batch in blob_batches:
            with self.client.batch():
                for blob in batch:
                    blob.delete()

    def make_public(self, blob_path: str) -> Blob:
        blob = self.get_bucket().blob(blob_path)
        if blob.exists():
            blob.make_public()
        return blob

    def make_private(self, blob_path: str) -> Blob:
        blob = self.get_bucket().blob(blob_path)
        if blob.exists():
            blob.make_private()
        return blob


gs_client = GoogleCloudClient(BUCKET_NAME)


# google storage paths

# streams
def gs_playlist_path(stream_id, new: bool = False):
    return os.path.join(STREAMS_FOLDER, str(stream_id), "playlist_new.m3u8" if new else "playlist.m3u8")


def gs_playlist_path_json(stream_id, new: bool = False):
    return os.path.join(STREAMS_FOLDER, str(stream_id), "playlist_new.json" if new else "playlist.json")


def gs_torrent_path(stream_id, chunk_number: int):
    return os.path.join(STREAMS_FOLDER, str(stream_id), "torrents", f"{chunk_number}.torrent")


def gs_chunk_path(stream_id, chunk_filename: str):
    return os.path.join(STREAMS_FOLDER, str(stream_id), "chunks", chunk_filename)


def gs_thumbnail_path(stream_id):
    return os.path.join(STREAMS_FOLDER, str(stream_id), "thumbnail.jpg")


# profile pics
def gs_profile_pics_path(filename: str):
    return os.path.join(PROFILE_PICS_FOLDER, filename)


# panel images
def gs_panel_images_path(filename: str):
    return os.path.join(PANEL_IMAGES_FOLDER, filename)


# emoticons map
def gs_emoticons_map_path():
    return os.path.join(STATIC_FOLDER, "emoticons.json")
