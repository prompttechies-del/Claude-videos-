#!/bin/bash
# usage: finish.sh DAY   (after frames v<DAY>/f/ and overlay v<DAY>/o/ exist)
D=$1; E=/tmp/claude-0/-home-user-Claude-videos-/0301aef4-c249-512f-8dcb-48f473421570/scratchpad/ep; V=$E/v$D
T=$(python3 -c "import json;print(json.load(open('$V/timing.json'))['T'])")
O=/home/user/Claude-videos-/videos/ai/reels-30day-3d/day$D-3d.mp4
ffmpeg -v error -y -f lavfi -i color=c=black:s=2160x3840:r=24:d=$T -framerate 24 -i $V/f/f%04d.png -framerate 24 -i $V/o/f%06d.png -i $V/voice_mix.wav -i $V/sfx.wav -filter_complex "[1:v]scale=2160:3840:flags=lanczos,unsharp=5:5:0.6,eq=saturation=1.08[b];[0:v][b]overlay=0:0:eof_action=repeat[bb];[bb][2:v]overlay=0:0:eof_action=repeat,format=yuv420p[v];[3:a]apad[vo];[4:a]volume=0.5[s];[vo][s]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[a]" -map "[v]" -map "[a]" -t $T -c:v libx264 -crf 17 -preset medium -profile:v high -level 5.2 -r 24 -c:a aac -b:a 192k -movflags +faststart $O
python3 /home/user/Claude-videos-/.claude/skills/free-4k-video-render/scripts/verify.py $O --w 2160 --h 3840 --audio yes --platform reels
ffmpeg -v error -y -i $O -vf "fps=1/1.5,scale=200:-1,tile=17x1" -frames:v 1 $V/final.jpg
# free disk once the video exists and passed verify
if [ -s $O ] && [ -f $V/final.jpg ]; then rm -rf $V/f $V/o; fi
