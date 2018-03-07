import math

import subprocess


SEGMENT_SECONDS = 6


def make_master_manifest():
    manifest = [
        '#EXTM3U',
        '#EXT-X-VERSION:3',
        '#EXT-X-INDEPENDENT-SEGMENTS',
        '#EXT-X-STREAM-INF:BANDWIDTH=6140324,AVERAGE-BANDWIDTH=5116937,VIDEO-RANGE=SDR,CODECS="avc1.64001f,mp4a.40.2",RESOLUTION=1280x720,FRAME-RATE=25.000',
        'playlist.m3u8',
    ]
    return manifest


def make_playlist_manifest(duration):
    manifest = [
        '#EXTM3U',
        '#EXT-X-PLAYLIST-TYPE:VOD',
        '#EXT-X-VERSION:3',
        '#EXT-X-TARGETDURATION:{}'.format(SEGMENT_SECONDS),
        '#EXT-X-MEDIA-SEQUENCE:0'
    ]

    num_segments = math.ceil(duration / SEGMENT_SECONDS)
    for i in range(num_segments):
        if duration >= SEGMENT_SECONDS:
            segment_length = SEGMENT_SECONDS
            duration -= SEGMENT_SECONDS
        else:
            segment_length = duration
        manifest.append('#EXTINF:{:.4f}, nodesc'.format(
            round(float(segment_length), 4)))
        manifest.append('{}.ts'.format(i))
    manifest.append('#EXT-X-ENDLIST')
    return manifest


def get_duration_seconds(path):
    output = subprocess.run(['ffmpeg', '-i', path],
                            stderr=subprocess.PIPE)
    for l in output.stderr.decode().split('\n'):
        line = l.strip()
        if line.startswith('Duration: '):
            duration_str = line.split()[1][:-1]
            hours, minutes, seconds = duration_str.split(':')

            hours = int(hours)
            minutes = int(minutes)
            seconds = float(seconds)

            duration = \
                (hours * 60 * 60) + \
                (minutes * 60) + \
                (seconds)

            return duration
