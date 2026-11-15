# Episode pipeline (CLAWD: The Desk Files)
Blender (EEVEE, headless) + Kokoro voices + HTML kinetic text + ffmpeg. Needs `assets` from the repo and a scratchpad with the desk scene (`d2head.py`), fonts and logos.
Per day: spec.json (voice lines) -> `voice.py DAY` -> cards.json + ep.json -> `gen_overlay.py`, `gen_scene.py`, `gen_sfx.py` -> `run_ep.sh DAY` (renders, assembles, verifies).
Days 4-16 were hand-written scenes (days/NN/dNN.py); days 17-30 are generated from ep.json.
