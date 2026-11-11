"""Generate one photoreal 9:16 still per shot. Usage: gen_image.py shots.json outdir"""
import json, os, shutil, sys
from gradio_client import Client

shots, out = json.load(open(sys.argv[1])), sys.argv[2]
os.makedirs(out, exist_ok=True)
client = Client("https://mcp-tools-flux-1-krea-dev.hf.space/", verbose=False)
for s in shots:
    path = f"{out}/{s['id']}.png"
    if os.path.exists(path):
        continue
    try:
        r = client.predict(prompt=s["image_prompt"], seed=0, randomize_seed=True, width=576, height=1024,
                           guidance_scale=4.5, num_inference_steps=24, api_name="/infer")
        shutil.copy(r[0], path)
        print("OK", s["id"], flush=True)
    except Exception as e:
        print("FAIL", s["id"], str(e)[:200], flush=True)
        if "quota" in str(e).lower() or "limit" in str(e).lower():
            break
