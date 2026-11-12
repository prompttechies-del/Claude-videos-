#!/usr/bin/env bash
# audio_polish.sh loudnorm|denoise|duck|fade ...   (free ffmpeg audio finishing)
#   loudnorm in out          -14 LUFS, -1 dBTP (YouTube/Spotify)
#   denoise  in out          FFT noise reduction
#   duck     voice music out music ducks under the voice (sidechain), then loudnorm
#   fade     in out          0.5 s fade in, 0.8 s fade out
set -euo pipefail
cmd=$1; shift
case "$cmd" in
  loudnorm) ffmpeg -v error -y -i "$1" -af loudnorm=I=-14:TP=-1:LRA=11 -ar 48000 "$2";;
  denoise)  ffmpeg -v error -y -i "$1" -af afftdn=nf=-25 "$2";;
  duck)     ffmpeg -v error -y -i "$1" -i "$2" -filter_complex "[0:a]aformat=channel_layouts=stereo,asplit=2[v][sc];[1:a]aformat=channel_layouts=stereo,volume=0.6[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];[v][md]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1:LRA=11" -ar 48000 "$3";;
  fade)     d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"); st=$(awk -v d="$d" 'BEGIN{print d-0.8}')
            ffmpeg -v error -y -i "$1" -af "afade=t=in:d=0.5,afade=t=out:st=$st:d=0.8" "$2";;
  *) echo "usage: audio_polish.sh loudnorm|denoise|duck|fade ..." >&2; exit 2;;
esac
echo "audio -> ${@: -1}"
