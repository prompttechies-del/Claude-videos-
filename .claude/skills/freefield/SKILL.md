---
name: freefield
description: Generate cinematic images, video clips, VFX, voice and music with Freefield, the open-source Higgsfield rebuild vendored in freefield/. Use when a video needs AI footage (text or image to video, camera moves, cinema-studio stills, upscaling, lip sync, music, sound effects) and a Freefield GPU backend is configured. Use instead of Higgsfield, which is paid.
---

# Freefield

`freefield/` is a copy of https://github.com/neuregex/freefield (MIT, commit
`f3d32ce`). It is 120 ComfyUI apps on open weights, each a folder in `freefield/apps/`
with an `app.json` (inputs) and a workflow. Read `freefield/README.md` for the full
app table and setup.

## It needs a GPU backend

Freefield does not generate anything by itself. It sends workflows to a ComfyUI
backend that the user must provide:

- **Modal** (cloud GPU, pay per second; about $2-4 per GPU hour per the README), or
- **their own GPU** with about 24 GB of memory (`tools/local_backend.py`).

A 4 GB laptop GPU and this cloud session (no GPU) cannot run it. Check before use:

```sh
cd freefield && grep -s COMFY_BASE_URL .env   # empty or missing: no backend yet
```

If there is no backend, say so, and use the `cinematic-shorts` skill instead (free
Hugging Face quota). Do not pretend Freefield ran.

## Setting up a backend (user steps, once)

Follow "Run it" in `freefield/README.md`: `python tools/doctor.py` lists what is
missing; then Modal login, `python tools/setup_token.py`, the Hugging Face secret,
`modal run infra/modal_app.py::download --pack <pack>`, `modal deploy infra/modal_app.py`,
and `COMFY_BASE_URL` in `freefield/.env`. Secrets go in `.env` or the environment's
network secrets, never in chat or in git (`.env` is gitignored).

## Running an app

Needs Node 22.6+. From `freefield/`:

```sh
npm install
npm run apps                                   # list apps and their status
npm run app -- <id> --set key=value --file key=path --out <dir>
```

Input ids for `--set` and `--file` are the `inputs[].id` values in
`apps/<id>/app.json`. Results and a `meta.json` land in `out/history/<run>/`.

## Apps for cinematic, realistic shorts

| Need | App | Notes |
|---|---|---|
| Photoreal still | `create-image`, `cinema-studio` | cinema-studio adds camera body, lens, aperture, lighting, palette |
| Still to moving shot with sound | `cinema-video` | up to 3 camera moves; one move holds best; needs ~44 GB |
| Text or image to video | `video-t2v`, `video`, `h3-video`, `h3-photo` | LTX-2.5 fits 24 GB; H3 needs more |
| Camera move on a still | `camera-moves` | Wan 2.2 Fun Camera, fits 24 GB by phases |
| Longer shot | `extend-video` | continues from the last frame |
| Sharper output | `upscale`, `upscale-video` | SeedVR2, small |
| Talking character | `speak`, `talking` | lip sync from a line or an audio file |
| Music, sound effects | `music`, `sfx` | check each model's license in its `app.json` before commercial use |

Then cut the shots together with the edit step of the `cinematic-shorts` skill
(`.claude/skills/cinematic-shorts/scripts/edit.py`): grade, letterbox, titles, voice, music.

## Rules

- Each model has its own license, listed in its `app.json`; some are non-commercial.
  Check before using output in monetised content.
- Do not generate real people's likenesses without consent (face swap, character
  swap, lip sync apps).
- Keep the vendored copy unmodified; to update, re-copy from upstream and change the
  commit above.
