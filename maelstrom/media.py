import functools
import hashlib

from . import hls, ffmpeg

STREAM_INFO = {
    'BANDWIDTH': 6140324,
    'AVERAGE-BANDWIDTH': 5116937,
    'VIDEO-RANGE': 'SDR',
    'CODECS': ['avc1.64001f', 'mp4a.40.2'],
    'RESOLUTION': '1280x720',
    'FRAME-RATE': 25.000
}


class Video:

    def __init__(self, path):
        self.path = path.resolve()

        h = hashlib.sha256()
        h.update(str(self.path).encode())
        self.media_id = h.hexdigest()

    @property
    @functools.lru_cache(1)
    def manifest(self):
        seconds = ffmpeg.get_duration_seconds(self.path)

        manifest = hls.MasterManifest()
        manifest.add_variant(
            hls.VariantManifest(
                'onlyquality',
                STREAM_INFO,
                seconds
            )
        )
        return manifest
