#!/usr/bin/env python3
"""Final verification. Usage:
  verify.py <file> [--w W --h H] [--fps F] [--audio yes|no] [--platform youtube|reels|tiktok|linkedin|x|square]
Fails (exit 1) on wrong resolution, fps mismatch, missing audio, true peak above -1 dBTP, or a file over the platform limit."""
import argparse, json, os, re, subprocess, sys

LIMITS = {"youtube": 256 * 1024**3, "reels": 4 * 1024**3, "tiktok": 4 * 1024**3, "linkedin": 5 * 1024**3, "x": 512 * 1024**2, "square": 4 * 1024**3}

def probe(f):
    return json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", f]))

def true_peak(f):
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", f, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rfind("Summary:"):] if "Summary:" in r else ""
    pk = re.search(r"True peak:\s*Peak:\s*(-?[\d.]+|-inf)", tail); il = re.search(r"I:\s*(-?[\d.]+) LUFS", tail)
    return (float(pk.group(1)) if pk and pk.group(1) != "-inf" else None, float(il.group(1)) if il else None)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--w", type=int); ap.add_argument("--h", type=int)
    ap.add_argument("--fps", type=float); ap.add_argument("--audio", choices=["yes", "no"]); ap.add_argument("--platform", choices=list(LIMITS)); a = ap.parse_args()
    rows, ok = [], True
    def check(name, passed, detail):
        nonlocal ok; ok = ok and passed; rows.append(("✅" if passed else "❌", name, detail))
    if not os.path.exists(a.file) or os.path.getsize(a.file) == 0:
        print(f"❌ {a.file}: file missing or empty"); sys.exit(1)
    p = probe(a.file); v = next((s for s in p["streams"] if s["codec_type"] == "video"), None); au = next((s for s in p["streams"] if s["codec_type"] == "audio"), None)
    size = os.path.getsize(a.file); dur = float(p["format"].get("duration", 0))
    if not v: check("video stream", False, "none found")
    else:
        w, h = v["width"], v["height"]; n, d = v["r_frame_rate"].split("/"); fps = float(n) / float(d)
        check("resolution", (a.w is None or w == a.w) and (a.h is None or h == a.h), f"{w}x{h}" + (f" (expected {a.w}x{a.h})" if a.w else ""))
        check("frame rate", a.fps is None or abs(fps - a.fps) < 0.02, f"{fps:.3f} fps" + (f" (expected {a.fps:g})" if a.fps else ""))
        rows.append(("ℹ️ ", "video", f"{v['codec_name']} {v.get('pix_fmt', '')}, {dur:.2f} s"))
    if a.audio == "yes": check("audio present", au is not None, f"{au['codec_name']} {au.get('sample_rate', '')} Hz" if au else "missing but expected")
    elif a.audio == "no": check("no audio", au is None, "none" if au is None else "unexpected audio stream")
    if au:
        pk, il = true_peak(a.file)
        check("true peak ≤ -1 dBTP", pk is None or pk <= -1.0, "silent" if pk is None else f"{pk:.1f} dBTP" + (f", {il:.1f} LUFS" if il is not None else ""))
    if a.platform: check(f"size ≤ {a.platform} limit", size <= LIMITS[a.platform], f"{size / 1024**2:.1f} MB (limit {LIMITS[a.platform] / 1024**2:.0f} MB)")
    else: rows.append(("ℹ️ ", "size", f"{size / 1024**2:.1f} MB"))
    print(f"{'✅ PASS' if ok else '❌ FAIL'}  {a.file}")
    for mark, name, detail in rows: print(f"   {mark} {name:<22} {detail}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__": main()
