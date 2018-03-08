#!/bin/sh
MEDIA_ID="$1"
VARIANT_ID="$2"
FILE="$3"

ffmpeg \
    -noaccurate_seek -f matroska \
    -i file:"${FILE}" \
    -threads 0 -map 0:0 -map 0:1 -map -0:s -codec:v:0 copy \
    -bsf:v h264_mp4toannexb -copyts -vsync -1 -codec:a:0 aac -strict experimental \
    -ac 2 -ab 384000  -f segment -max_delay 5000000 -avoid_negative_ts disabled \
    -map_metadata -1 -map_chapters -1 -start_at_zero -segment_time 6  \
    -individual_header_trailer 0 -break_non_keyframes 1 -segment_format mpegts \
    -segment_list_type m3u8 -segment_start_number 0 \
    -y "transcode/"${MEDIA_ID}"/$"{VARIANT_ID}"_%d.ts"
