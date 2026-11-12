#!/usr/bin/env bash
# finish_visual.sh watermark|sharpen|grain|lut|stitch|thumb ...
#   watermark in logo.png out      logo bottom-right at 80% opacity
#   sharpen   in out               light sharpen after an upscale
#   grain     in out               fine film grain (premium feel, no gradient banding)
#   lut       in brand.cube out    colour grade with a 3D LUT
#   stitch    intro main outro out 0.5 s crossfades (video + audio)
#   thumb     in outdir            sharpest scene-change frame -> 1280x720 JPG + full-size PNG
set -euo pipefail
cmd=$1; shift; COPYA=(-c:a copy)
case "$cmd" in
  watermark) ffmpeg -v error -y -i "$1" -i "$2" -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.8[l];[0:v][l]overlay=W-w-60:H-h-60" "${COPYA[@]}" "$3";;
  sharpen)   ffmpeg -v error -y -i "$1" -vf unsharp=5:5:0.6 "${COPYA[@]}" "$2";;
  grain)     ffmpeg -v error -y -i "$1" -vf noise=alls=4:allf=t "${COPYA[@]}" "$2";;
  lut)       ffmpeg -v error -y -i "$1" -vf "lut3d=$2" "${COPYA[@]}" "$3";;
  stitch)    d1=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"); d2=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$2")
             o1=$(awk -v a="$d1" 'BEGIN{print a-0.5}'); o2=$(awk -v a="$d1" -v b="$d2" 'BEGIN{print a+b-1.0}')
             ffmpeg -v error -y -i "$1" -i "$2" -i "$3" -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=$o1[x];[x][2:v]xfade=transition=fade:duration=0.5:offset=$o2[v];[0:a][1:a]acrossfade=d=0.5[y];[y][2:a]acrossfade=d=0.5[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p "$4";;
  thumb)     mkdir -p "$2"; ffmpeg -v error -y -i "$1" -vf "select='gt(scene,0.3)',thumbnail=50" -frames:v 1 -update 1 "$2/thumb-full.png" || ffmpeg -v error -y -ss 1 -i "$1" -frames:v 1 "$2/thumb-full.png"
             ffmpeg -v error -y -i "$2/thumb-full.png" -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720" -q:v 2 "$2/thumb-1280x720.jpg";;
  *) echo "usage: finish_visual.sh watermark|sharpen|grain|lut|stitch|thumb ..." >&2; exit 2;;
esac
echo "done: ${@: -1}"
