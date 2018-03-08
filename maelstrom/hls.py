import math


SEGMENT_SECONDS = 6


class Manifest:

    def __init__(self):
        self.lines = []

    @property
    def text(self):
        return '\n'.join(self.lines)


class MasterManifest(Manifest):

    STREAM_INFO_KEYS = (
        'BANDWIDTH',
        'AVERAGE-BANDWIDTH',
        'VIDEO-RANGE',
        'CODECS',
        'RESOLUTION',
        'FRAME-RATE'
    )

    def __init__(self):
        super().__init__()
        self.lines.extend([
            '#EXTM3U',
            '#EXT-X-VERSION:3',
            '#EXT-X-INDEPENDENT-SEGMENTS'
        ])
        self.variants = {}

    def add_variant(self, variant):
        self.variants[variant.variant_id] = variant
        stream_info = []

        for key in self.STREAM_INFO_KEYS:
            value = variant.stream_info.get(key)
            if value is None:
                continue
            elif isinstance(value, (int, str)):
                result = f'{key}={value}'
            elif isinstance(value, list):
                result = '{}="{}"'.format(key, ','.join(value))
            elif isinstance(value, float):
                result = '{}={:.3f}'.format(key, value)
            stream_info.append(result)

        if stream_info:
            self.lines.append('#EXT-X-STREAM-INF:{}'.format(
                ','.join(stream_info)))
        self.lines.append(f'{variant.variant_id}.m3u8')


class VariantManifest(Manifest):

    def __init__(self, variant_id, stream_info, duration):
        super().__init__()
        self.variant_id = variant_id
        self.duration = duration
        self.stream_info = stream_info

        self.lines.extend([
            '#EXTM3U',
            '#EXT-X-PLAYLIST-TYPE:VOD',
            '#EXT-X-VERSION:3',
            '#EXT-X-TARGETDURATION:{}'.format(SEGMENT_SECONDS),
            '#EXT-X-MEDIA-SEQUENCE:0'
        ])

        num_segments = math.ceil(duration / SEGMENT_SECONDS)
        for i in range(num_segments):
            if duration >= SEGMENT_SECONDS:
                segment_length = SEGMENT_SECONDS
                duration -= SEGMENT_SECONDS
            else:
                segment_length = duration
            self.lines.append('#EXTINF:{:.4f}, nodesc'.format(
                round(float(segment_length), 4)))
            self.lines.append(f'{self.variant_id}_{i}.ts')
        self.lines.append('#EXT-X-ENDLIST')
