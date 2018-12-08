import asyncio


async def transcode(source, variant, media_id, output, segment_start):
    output = output.joinpath(media_id, variant)
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
        '-initial_offset', str(segment_start),
        '-y', f'{output}/%d.ts'
    ]
    proc = await asyncio.create_subprocess_exec(*proc_args)
    await proc.wait()
