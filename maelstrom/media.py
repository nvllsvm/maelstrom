from maelstrom import hls, ffmpeg

STREAM_INFO = {
    'BANDWIDTH': 6140324,
    'AVERAGE-BANDWIDTH': 5116937,
    'VIDEO-RANGE': 'SDR',
    'CODECS': ['avc1.64001f', 'mp4a.40.2'],
    'RESOLUTION': '1280x720',
    'FRAME-RATE': 25.000
}


class Video:

    def __init__(self, media_id, path):
        self.media_id = media_id
        self.path = path.resolve()
        self.seconds = ffmpeg.get_duration_seconds(path)
        self.manifest = hls.MasterManifest()
        self.manifest.add_variant(hls.VariantManifest(
            'onlyquality',
            STREAM_INFO,
            self.seconds))
