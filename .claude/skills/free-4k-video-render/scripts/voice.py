"""Natural free voice-over with Kokoro (offline, CPU), plus light studio processing.
Usage: python voice.py <lines.json> <outdir> [voice=af_heart]
lines.json: ["First line.", "Second line.", ...]  ->  outdir/l0.wav, l1.wav, ... and durations.json
Most natural Kokoro voices: af_heart (best), af_bella; male: am_michael, am_fenrir. English and Hindi; no Telugu."""
import sys, os, json, subprocess
import soundfile as sf
from kokoro_onnx import Kokoro
lines, out = json.load(open(sys.argv[1])), sys.argv[2]; voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
os.makedirs(out, exist_ok=True)
base = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
    if not os.path.exists(f"{out}/{f}"): subprocess.run(["curl", "-sSL", "-o", f"{out}/{f}", base + f], check=True)
k = Kokoro(f"{out}/kokoro-v1.0.onnx", f"{out}/voices-v1.0.bin"); durs = []
FX = "highpass=f=75,lowpass=f=13000,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.2:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=3,aecho=0.85:0.6:28|47:0.10|0.06,alimiter=limit=0.95"
for i, t in enumerate(lines):
    a, sr = k.create(t, voice=voice, speed=0.98, lang="en-us"); sf.write(f"{out}/raw{i}.wav", a, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{out}/raw{i}.wav", "-af", FX, "-ar", "44100", f"{out}/l{i}.wav"], check=True)
    durs.append(len(a) / sr); print(i, round(durs[-1], 2))
json.dump(durs, open(f"{out}/durations.json", "w"))
