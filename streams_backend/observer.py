import io
import logging
import os
import re
import threading
import time
from decimal import Decimal

from django.db import transaction
from moviepy.video.io.VideoFileClip import VideoFileClip
from sentry_sdk import capture_exception
from torf import Torrent
from watchgod import RegExpWatcher, watch, Change

CHUNK_FILENAME_PATTERN = r"^[0-9]+\.ts$"
UPDATE_THUMBNAIL_EVERY = 5
CHUNKS_PATH = "/var/chunks"
THUMBNAILS_PATH = "/tmp/thumbnails"
M3U8_PATTERN = r".*\.m3u8$"


def handle_playlist_update(src_path: str):
    rtmp_playlist_path = os.path.abspath(src_path)
    basedir: str = os.path.dirname(rtmp_playlist_path)
    try:
        stream_obj: Stream = Stream.objects.get(pk=os.path.basename(basedir))
    except ValueError as err:
        capture_exception(err)
        logging.error("Stream id is not valid UUID")
        return
    tracker_urls = [tracker.url for tracker in Tracker.objects.filter(is_active=True).all()]
    with open(rtmp_playlist_path) as f:
        chunk_filenames = re.findall(CHUNK_FILENAME_PATTERN, f.read(), re.MULTILINE)
        print(chunk_filenames)
        if not chunk_filenames:
            return
        chunk_filename = chunk_filenames[-1]
        start_time = time.time()
        chunk_number: int = int(chunk_filename.rstrip(".ts"))
        if not Chunk.objects.filter(stream=stream_obj, number=chunk_number).exists():
            try:
                with transaction.atomic():
                    if stream_obj.viewers and stream_obj.viewers < config.TARGET_SEED_USERS:
                        cloud_url_prob = stream_obj.viewers / config.TARGET_SEED_USERS
                    else:
                        cloud_url_prob = Decimal(config.USE_CLOUD_PROB / 100) if config.USE_CLOUD_PROB else 0
                    chunk_path = os.path.join(basedir, chunk_filename)
                    secret_filename = f"{chunk_number}_{random_string()}.ts"
                    new_chunk: Chunk = \
                        Chunk.objects.create(stream=stream_obj, number=chunk_number, filename=secret_filename, prob=cloud_url_prob)
                    t = Torrent(path=chunk_path, trackers=tracker_urls, webseeds=[new_chunk.file_url, ], piece_size=2 ** 20)
                    t.generate()
                    new_chunk.magnet_link = t.magnet()
                    with io.BytesIO() as torrent_file:
                        t.write_stream(torrent_file)
                        gs_client.upload_file(torrent_file, gs_torrent_path(stream_obj.id, new_chunk.number))
                    with VideoFileClip(chunk_path) as chunk_clip:
                        new_chunk.duration = Decimal(chunk_clip.duration)
                        if new_chunk.number % UPDATE_THUMBNAIL_EVERY == 0:
                            thumbnail_path = f"/tmp/thumbnails/{stream_obj.id}.jpg"
                            time_mark = chunk_clip.duration * 0.05
                            chunk_clip.save_frame(thumbnail_path, t=time_mark)
                            gs_client.upload_file(thumbnail_path, gs_thumbnail_path(stream_obj.id))
                    gs_client.upload_file(chunk_path, gs_chunk_path(stream_obj.id, new_chunk.filename), content_type="video/MP2T")
                    new_chunk.is_public = True
                    new_chunk.save()
                    stream_obj.update_playlist()
                    logging.info(f"new chunk: {str(stream_obj.id)[0:5]}/{chunk_number} in {round(time.time() - start_time, 2)}s")
            except Exception as err:
                capture_exception(err)
                logging.error(err)


def observe_playlists():
    for changes in watch(CHUNKS_PATH, watcher_cls=RegExpWatcher, watcher_kwargs=dict(re_files=M3U8_PATTERN)):
        for change in changes:
            if change[0] != Change.deleted:
                threading.Thread(target=handle_playlist_update, kwargs=dict(src_path=change[1])).start()


def setup_django_app():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

    import django
    django.setup()


def main():
    for path in [CHUNKS_PATH, THUMBNAILS_PATH]:
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError as e:
                capture_exception(e)
                logging.error(e)

    try:
        logging.info("Waiting chunks...")
        observe_playlists()
    except KeyboardInterrupt:
        logging.info("Received exit, exiting")


if __name__ == "__main__":
    setup_django_app()
    from streams.models import Chunk, Tracker, Stream
    from file_storages.google_cloud import gs_client, gs_torrent_path, gs_thumbnail_path, gs_chunk_path
    from common.utils import random_string
    from constance import config

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    main()
