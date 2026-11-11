"""Cut the cinematic short. Usage: edit.py shots.json outdir final.mp4"""
import json, os, subprocess, sys, wave
import numpy as np

shots, out, final = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
FPS, XF, FONT = 30, 0.6, "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))

# Each shot lasts as long as its narration plus a breath, at least 4 seconds.
lens = [max(4.0, (dur(f"{out}/{s['id']}.wav") if os.path.exists(f"{out}/{s['id']}.wav") else 0) + 1.2) for s in shots]
total = sum(lens) - XF * (len(shots) - 1)

# Ambient music bed: slow pads and a low pulse.
sr = 44100; n = int(sr * (total + 1)); t = np.arange(n) / sr; m = np.zeros(n)
for i, chord in enumerate([[73.4, 110, 146.8, 220], [65.4, 98, 130.8, 196], [87.3, 130.8, 174.6, 261.6], [55, 82.4, 110, 164.8]] * 20):
    a, b = int(i * 6 * sr), int(min(n, (i * 6 + 6.5) * sr))
    if a >= n: break
    tt = t[a:b] - i * 6; env = np.minimum(tt / 2, 1) * np.minimum((6.5 - tt) / 1.5, 1)
    m[a:b] += sum(0.1 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2.01 * f * tt)) for f in chord)
m /= np.abs(m).max() * 1.2
w = wave.open(f"{out}/music.wav", "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((m * 32767).astype(np.int16).tobytes()); w.close()

ins, fc, at, starts = [], [], 0.0, []
for i, (s, L) in enumerate(zip(shots, lens)):
    clip, img = f"{out}/{s['id']}.mp4", f"{out}/{s['id']}.png"
    fit = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
    if os.path.exists(clip):
        ins += ["-i", clip]; slow = L / dur(clip)
        fc.append(f"[{i}:v]setpts={max(slow, 1):.3f}*PTS,{fit},fps={FPS},trim=duration={L:.2f},setsar=1[s{i}]")
    else:  # no clip: slow push-in on the still
        ins += ["-loop", "1", "-t", f"{L:.2f}", "-i", img]; fr = int(L * FPS)
        fc.append(f"[{i}:v]scale=2160:3840:flags=lanczos,zoompan=z='1+0.10*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={FPS},setsar=1[s{i}]")
    starts.append(at); at += L - XF
prev, off = "s0", 0.0
for i in range(1, len(shots)):
    off += lens[i - 1] - XF
    fc.append(f"[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]"); prev = f"x{i}"
look = "eq=contrast=1.08:saturation=0.92:gamma=0.97,colorbalance=rs=0.04:bs=-0.04:bh=0.03,vignette=PI/4.5,noise=alls=7:allf=t,drawbox=0:0:iw:150:black:fill,drawbox=0:ih-150:iw:150:black:fill"
titles = ""
for s, st, L in zip(shots, starts, lens):
    if s.get("title"):
        txt = s["title"].replace("'", "’").replace(":", "\\:")
        titles += f",drawtext=fontfile={FONT}:text='{txt}':fontsize=58:fontcolor=white@0.95:x=(w-text_w)/2:y=h-330:alpha='min(1,max(0,(t-{st + 0.6:.2f})/0.8))*min(1,max(0,({st + L - 0.8:.2f}-t)/0.6))'"
fc.append(f"[{prev}]{look}{titles},fade=t=in:d=0.8,fade=t=out:st={total - 1:.2f}:d=1,format=yuv420p[v]")
k = len(shots); voices = []
for s, st in zip(shots, starts):
    p = f"{out}/{s['id']}.wav"
    if os.path.exists(p):
        ins += ["-i", p]; fc.append(f"[{k}:a]adelay={int((st + 0.5) * 1000)}:all=1[a{k}]"); voices.append(f"[a{k}]"); k += 1
ins += ["-i", f"{out}/music.wav"]
fc.append(f"[{k}:a]volume=0.5,afade=t=in:d=1.5,afade=t=out:st={total - 2:.2f}:d=2[mus]")
if voices:
    fc.append("".join(voices) + f"amix=inputs={len(voices)}:normalize=0,volume=1.6[vo];[vo][mus]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.95[a]")
else:
    fc.append("[mus]anull[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
               "-t", f"{total:.2f}", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", final], check=True)
print("wrote", final, round(total, 1), "s")
