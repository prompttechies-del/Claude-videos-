"""Animate each still into a ~5s clip. Usage: gen_clip.py shots.json outdir"""
import json, os, shutil, sys
from gradio_client import Client, handle_file

shots, out = json.load(open(sys.argv[1])), sys.argv[2]
client = Client("https://zerogpu-aoti-wan2-2-fp8da-aoti-faster.hf.space/", verbose=False)
for s in shots:
    img, path = f"{out}/{s['id']}.png", f"{out}/{s['id']}.mp4"
    if os.path.exists(path) or not os.path.exists(img):
        continue
    try:
        v = client.predict(input_image=handle_file(img), prompt=s["motion_prompt"], steps=6,
                           duration_seconds=5, api_name="/generate_video")[0]
        shutil.copy(v.get("video") if isinstance(v, dict) else v, path)
        print("OK", s["id"], flush=True)
    except Exception as e:
        print("FAIL", s["id"], str(e)[:200], flush=True)
        if "quota" in str(e).lower() or "limit" in str(e).lower():
            break
