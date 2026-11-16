#!/bin/bash
E=/tmp/claude-0/-home-user-Claude-videos-/0301aef4-c249-512f-8dcb-48f473421570/scratchpad/ep; cd $E
pgrep -f "queue3.sh" >/dev/null && echo "queue running" || { (nohup setsid ./queue3.sh > queue3.log 2>&1 < /dev/null &); echo "restarted queue"; }
echo "uptime: $(uptime -p)"
for D in $(cat ids.txt); do
  b=$([ -f v$D/sfx.wav ] && echo built || echo NOT-BUILT); f=$([ -f v$D/final.jpg ] && [ ! -f v$D/redo ] && echo done || echo todo); s=$(grep -qx $D sent2.txt 2>/dev/null && echo sent || echo unsent)
  [ "$b $f $s" = "built done unsent" ] && echo "SEND $D"
  [ "$b" = "NOT-BUILT" ] && echo "BUILD $D"
done | head -40
