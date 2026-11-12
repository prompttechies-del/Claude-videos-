#!/usr/bin/env bash
# autocaptions.sh <audio|video> <out.srt> [--burn <video> <out.mp4>]
# Local, free speech-to-text: faster-whisper (pip) or whisper.cpp (whisper-cli + a ggml model in $WHISPER_MODEL).
# Both download their model once from Hugging Face; if that host is blocked, say so and caption from the script text instead.
set -euo pipefail
IN=$1; SRT=$2; shift 2
if python3 -c "import faster_whisper" 2>/dev/null; then
  python3 - "$IN" "$SRT" <<'PY'
import sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="auto", compute_type="int8"); segs, _ = m.transcribe(sys.argv[1], vad_filter=True)
ts = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000 % 1000):03d}"
with open(sys.argv[2], "w") as f:
    for i, s in enumerate(segs, 1): f.write(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n\n")
PY
elif command -v whisper-cli >/dev/null 2>&1 && [ -f "${WHISPER_MODEL:-}" ]; then
  ffmpeg -v error -y -i "$IN" -ar 16000 -ac 1 /tmp/_ac.wav; whisper-cli -m "$WHISPER_MODEL" -f /tmp/_ac.wav -osrt -of "${SRT%.srt}" >/dev/null
else echo "❌ no local whisper: pip install faster-whisper (needs huggingface.co once) or install whisper.cpp and set WHISPER_MODEL" >&2; exit 1; fi
echo "captions -> $SRT (also upload it to YouTube as a separate file)"
if [ "${1:-}" = --burn ]; then
  ffmpeg -v error -y -i "$2" -vf "subtitles=$SRT:force_style='FontName=Inter,FontSize=18,Bold=1,Outline=2,Alignment=2,MarginV=120'" -c:a copy "$3"; echo "burned -> $3"; fi
