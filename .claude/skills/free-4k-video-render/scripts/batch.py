#!/usr/bin/env python3
"""Batch mode. Usage: batch.py jobs.json
jobs.json: [{"src": "...", "orientation": "9x16", "title": "My video", "music": "bed.mp3", "captions": "c.srt", "quality": "standard", "duration": 10}]
Each job renders to out/<slug>/<slug>.mp4 (music ducked + normalised, captions burned) and a summary table is printed."""
import json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); jobs = json.load(open(sys.argv[1])); rows = []
for j in jobs:
    slug = re.sub(r"[^a-z0-9]+", "-", (j.get("title") or os.path.basename(j["src"].rstrip("/"))).lower()).strip("-") or "video"
    os.makedirs(f"out/{slug}", exist_ok=True); out = f"out/{slug}/{slug}.mp4"; t0 = time.time()
    cmd = [f"{HERE}/render4k.sh", "--src", j["src"], "--orientation", j.get("orientation", "16x9"), "--quality", j.get("quality", "standard"), "--out", out]
    for k in ("fps", "duration", "comp"):
        if j.get(k): cmd += [f"--{k}", str(j[k])]
    if j.get("music"): cmd += ["--audio", j["music"]]
    if j.get("captions"): cmd += ["--captions", j["captions"]]
    ok = subprocess.run(cmd).returncode == 0; took = time.time() - t0
    if os.path.exists(out):
        p = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration,size", "-of", "json", out]))
        v = next(s for s in p["streams"] if "width" in s); rows.append((("✅" if ok else "❌"), out, f"{v['width']}x{v['height']}", f"{float(p['format']['duration']):.1f}s", f"{int(p['format']['size']) / 1024**2:.1f} MB", f"{took:.0f}s"))
    else: rows.append(("❌", out, "-", "-", "-", f"{took:.0f}s"))
w = [max(len(str(r[i])) for r in rows + [("", "file", "resolution", "duration", "size", "time")]) for i in range(6)]
print("\n" + "  ".join(h.ljust(w[i]) for i, h in enumerate(["", "file", "resolution", "duration", "size", "time"])))
for r in rows: print("  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))
sys.exit(0 if all(r[0] == "✅" for r in rows) else 1)
