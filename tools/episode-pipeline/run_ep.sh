#!/bin/bash
# usage: run_ep.sh DAY  -> renders 3D frames, overlay, then assembles
D=$1; E=/tmp/claude-0/-home-user-Claude-videos-/0301aef4-c249-512f-8dcb-48f473421570/scratchpad/ep; cd $E
N=$(python3 -c "import json,math;print(math.ceil(json.load(open('v$D/timing.json'))['T3']*24))")
mkdir -p v$D/f v$D/o
S0=0; while [ -s v$D/f/f$(printf %04d $S0).png ]; do S0=$((S0+1)); done; [ $S0 -gt 0 ] && S0=$((S0-1)) && rm -f v$D/f/f$(printf %04d $S0).png
[ $S0 -lt $N ] && DAY=$D NFR=$((N-S0)) blender -b -P run$D.py -- BLENDER_EEVEE 720 1280 6 //v$D/f/f# $S0 >> v$D/render.log 2>&1
[ $(ls v$D/o | wc -l) -gt 10 ] || (cd ../mg && node seek.mjs --src day${D}o.html --out ../ep/v$D/o --scale 2 --fps 24 --workers 1 --png 1 > /dev/null)
./finish.sh $D
