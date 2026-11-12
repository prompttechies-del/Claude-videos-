#!/bin/bash
# reel.sh <master 16:9 mp4> <soundtrack wav (story length)> <end-line voice wav> <brand dir> <captions.ass> <out.mp4> [scale=2] [story seconds=30]
# Vertical Reel: navy background, the full 16:9 video in a rounded glowing frame, logo icon top-right, title + tag,
# captions below the video, "Prompt Techies" at the bottom, then a 2.5 s white logo end card with the end line.
set -e
M=$1; A=$2; EV=$3; B=$4; CAP=$5; OUT=$6; s=${7:-2}; T=${8:-30}
W=$((1080*s)); VW=$((1040*s)); VH=$((585*s)); X=$((20*s)); VY=$((690*s)); RX=$((-4*s)); RY=$((VY-24*s))
FONTS=/mnt/skills/examples/canvas-design/canvas-fonts
cat > /tmp/reel_fc.txt <<FC
[0:v]fps=30,trim=duration=$T,setpts=PTS-STARTPTS,scale=$VW:$VH:flags=lanczos,format=rgba[vid];[7:v]format=gray[mk];[vid][mk]alphamerge[vr];
[8:v]loop=-1:size=1,fps=30,trim=duration=$T,format=rgba[bg];[bg][vr]overlay=$X:$VY[b1];[b1][9:v]overlay=$RX:$RY[b2];
[b2][2:v]overlay=W-w-$((6*s)):$((44*s))[b3];[b3][5:v]overlay=(W-w)/2:$((300*s))[b4];[b4][6:v]overlay=(W-w)/2:$((446*s))[b5];[b5][4:v]overlay=(W-w)/2:$((1748*s))[b6];
[b6]ass=$CAP:fontsdir=$FONTS,format=yuv420p,setsar=1[mv];
[1:v]fps=30,setsar=1,format=yuv420p,fade=t=in:d=0.4[e];[mv][e]concat=n=2:v=1:a=0[v];
[3:a]atrim=0:$T,aformat=sample_rates=44100:channel_layouts=stereo[a1];[10:a]adelay=300:all=1,apad=whole_dur=2.5,aformat=sample_rates=44100:channel_layouts=stereo,volume=1.3[a2];[a1][a2]concat=n=2:v=0:a=1[a]
FC
ffmpeg -v error -y -i "$M" -loop 1 -t 2.5 -i $B/end.png -i $B/icon.png -i "$A" -i $B/mark.png -i $B/title.png -i $B/tag.png -i $B/mask.png -i $B/bg.png -i $B/ring.png -i "$EV" \
  -filter_complex_script /tmp/reel_fc.txt -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset medium -profile:v high -level 5.2 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart "$OUT"
echo "reel -> $OUT"
