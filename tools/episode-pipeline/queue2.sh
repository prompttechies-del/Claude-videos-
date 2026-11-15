#!/bin/bash
# renders any built-but-unfinished day (17..30), picking up newly built ones; exits after 15 min with nothing to do
E=/tmp/claude-0/-home-user-Claude-videos-/0301aef4-c249-512f-8dcb-48f473421570/scratchpad/ep; cd $E; idle=0
while [ $idle -lt 90 ]; do
  NEXT=""; for D in 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do [ -f run$D.py ] && [ -f v$D/sfx.wav ] && [ ! -f v$D/final.jpg ] && NEXT=$D && break; done
  if [ -n "$NEXT" ]; then idle=0; mkdir -p v$NEXT; ./run_ep.sh $NEXT > v$NEXT/run.out 2>&1; else idle=$((idle+1)); sleep 10; fi
done
