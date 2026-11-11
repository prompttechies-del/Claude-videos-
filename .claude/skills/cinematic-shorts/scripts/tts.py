"""Narrate each shot's line with Kokoro. Usage: tts.py shots.json outdir [voice]"""
import json, os, subprocess, sys
import soundfile as sf
from kokoro_onnx import Kokoro

shots, out = json.load(open(sys.argv[1])), sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "am_michael"
base = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
    if not os.path.exists(f"{out}/{f}"):
        subprocess.run(["curl", "-sSL", "-o", f"{out}/{f}", base + f], check=True)
k = Kokoro(f"{out}/kokoro-v1.0.onnx", f"{out}/voices-v1.0.bin")
for s in shots:
    if s.get("line"):
        a, sr = k.create(s["line"], voice=voice, speed=0.95, lang="en-us")
        sf.write(f"{out}/{s['id']}.wav", a, sr)
        print(s["id"], round(len(a) / sr, 2), flush=True)
