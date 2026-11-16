#!/bin/bash
# renders, in order of ids.txt, every day that is built and (has no final.jpg OR is flagged redo); exits after 15 idle minutes
E=/tmp/claude-0/-home-user-Claude-videos-/0301aef4-c249-512f-8dcb-48f473421570/scratchpad/ep; cd $E; idle=0
while [ $idle -lt 90 ]; do
  NEXT=""; for D in $(cat ids.txt); do [ -f run$D.py ] && [ -f v$D/sfx.wav ] && { [ ! -f v$D/final.jpg ] || [ -f v$D/redo ]; } && NEXT=$D && break; done
  if [ -n "$NEXT" ]; then idle=0; [ -f v$NEXT/redo ] && rm -f v$NEXT/final.jpg; ./run_ep.sh $NEXT > v$NEXT/run.out 2>&1; [ -f v$NEXT/final.jpg ] || sleep 30; else idle=$((idle+1)); sleep 10; fi
done
