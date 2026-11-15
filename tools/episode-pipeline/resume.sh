#!/bin/bash
# Restart the render queue for every built-but-unfinished day (run<DAY>.py exists, final.jpg missing). Safe any time.
E=/tmp/claude-0/-home-user-Claude-videos-/0301aef4-c249-512f-8dcb-48f473421570/scratchpad/ep; cd $E
REM=""; for D in 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do [ -f run$D.py ] && [ -f v$D/sfx.wav ] && [ ! -f v$D/final.jpg ] && REM="$REM $D"; done
if pgrep -f "queue2.sh" >/dev/null; then echo "queue already running:$REM"; else
  [ -n "$REM" ] && (nohup setsid ./queue2.sh > queue.log 2>&1 < /dev/null &) && echo "restarted queue:$REM" || echo "nothing to render"; fi
echo "uptime: $(uptime -p)"; for D in 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do echo "day$D built=$([ -f v$D/sfx.wav ] && echo yes || echo no) frames=$(ls v$D/f 2>/dev/null | wc -l) final=$([ -f v$D/final.jpg ] && echo yes || echo no) sent=$(grep -qx $D sent.txt 2>/dev/null && echo yes || echo no)"; done
