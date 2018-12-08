import hashlib
import pathlib
import subprocess
import sys


OUTPUT = pathlib.Path('build/transcode')
OUTPUT.mkdir(parents=True, exist_ok=True)
SOURCE = pathlib.Path(sys.argv[1]).resolve()

VARIANT = 'onlyquality'
SEGMENT_START = 0


def hash_name(value):
    h = hashlib.sha256()
    h.update(value.encode())
    return h.hexdigest()


def _transcode(source, variant, output, segment_start):
    output = output.joinpath(hash_name(str(source)))
    output.mkdir(parents=True, exist_ok=True)

    proc_args = [
        'ffmpeg', '-noaccurate_seek', '-f', 'matroska', '-i', f'file:{source}',
        '-threads', '0', '-map', '0:0', '-map', '0:1', '-map', '-0:s',
        '-codec:v:0', 'copy', '-bsf:v', 'h264_mp4toannexb', '-copyts',
        '-vsync', '-1', '-codec:a:0', 'aac', '-strict', 'experimental',
        '-ac', '2', '-ab', '384000', '-f', 'segment', '-max_delay', '5000000',
        '-avoid_negative_ts', 'disabled', '-map_metadata', '-1',
        '-map_chapters', '-1', '-start_at_zero', '-segment_time', '6',
        '-individual_header_trailer', '0', '-break_non_keyframes', '1',
        '-segment_format', 'mpegts', '-segment_list_type', 'm3u8',
        '-segment_start_number', str(segment_start),
        '-y', f'{output}/{variant}_%d.ts'
    ]
    subprocess.run(proc_args, check=True)


_transcode(SOURCE, VARIANT, OUTPUT, SEGMENT_START)
