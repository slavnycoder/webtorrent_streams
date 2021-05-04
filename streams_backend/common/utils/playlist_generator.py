import logging
import math

logger = logging.getLogger(__name__)


class PlaylistGenerator(object):
    def __init__(self, playlist_entries=None, version=3, sequence=0):
        if not playlist_entries:
            raise AttributeError()

        self.end_playlist = False
        self.playlist_entries = playlist_entries
        self.version = version
        self.sequence = sequence
        self.duration = self.duration()

    def _generate_playlist_entries(self) -> str:
        playlist = ""
        for entry in self.playlist_entries:
            playlist += f"#EXTINF:{entry['duration']},\n{entry['path']}\n"
        return playlist

    def _m3u8_header_template(self) -> str:
        header = f"#EXTM3U\n#EXT-X-VERSION:{self.version}\n" \
                 f"#EXT-X-TARGETDURATION:{math.ceil(self.duration)}\n" \
                 f"#EXT-X-MEDIA-SEQUENCE:{self.sequence}\n"
        if self.end_playlist:
            return f"{header}\n#EXT-X-ENDLIST"
        else:
            return header

    def duration(self):
        max_duration = 0
        for entry in self.playlist_entries:
            max_duration = max(max_duration, entry.get('duration', 0))
        return max_duration

    def generate(self):
        playlist = self._m3u8_header_template() + self._generate_playlist_entries()
        return playlist
