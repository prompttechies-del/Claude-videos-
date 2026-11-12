#!/usr/bin/env bash
# export_all.sh <4k master> <outdir>: every platform version in parallel from one master, each verified.
# Aspect changes use a blurred-background pad; CROP=1 uses a centre crop instead.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); M=$1; O=${2:-out/exports}; mkdir -p "$O"; N=$(basename "${M%.*}")
HASA=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$M" | grep -c . || true)
A=(-an); [ "$HASA" -gt 0 ] && A=(-c:a aac -b:a 192k -ar 48000 -af loudnorm=I=-14:TP=-1.5:LRA=11)
fit(){ local w=$1 h=$2; if [ "${CROP:-0}" = 1 ]; then echo "[0:v]scale=$w:$h:force_original_aspect_ratio=increase,crop=$w:$h,setsar=1[v]";
  else echo "[0:v]split[a][b];[a]scale=$w:$h:force_original_aspect_ratio=increase,crop=$w:$h,boxblur=40[bg];[b]scale=$w:$h:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"; fi; }
job(){ local out=$1 w=$2 h=$3 crf=$4 plat=$5; shift 5
  ffmpeg -v error -y -i "$M" -filter_complex "$(fit $w $h)" -map "[v]" ${HASA:+-map 0:a:0?} "${A[@]}" -c:v libx264 -crf $crf -preset medium -pix_fmt yuv420p "$@" -movflags +faststart "$out" \
    && python3 "$HERE/verify.py" "$out" --w $w --h $h --audio $([ "$HASA" -gt 0 ] && echo yes || echo no) --platform $plat; }
job "$O/$N-youtube-4k.mp4"   3840 2160 18 youtube &
job "$O/$N-reels-4k.mp4"     2160 3840 18 reels &
job "$O/$N-reels-1080.mp4"   1080 1920 20 reels &
job "$O/$N-linkedin.mp4"     1920 1080 20 linkedin &
job "$O/$N-x.mp4"            1920 1080 21 x -maxrate 25M -bufsize 50M &
job "$O/$N-square.mp4"       1080 1080 20 square &
wait; echo "exports -> $O"
