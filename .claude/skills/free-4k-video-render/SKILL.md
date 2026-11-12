---
name: "free-4k-video-render"
description: "Render Claude-made videos (Remotion, HTML/canvas animations, image sequences) to 4K MP4 for free on the user's own machine. Also covers the one-command render script, multi-platform export, audio polish, free captions, visual finishing, batch mode, automatic verification and the Prompt Techies Reel layout."
---

# Free 4K Video Render

Goal: turn any video Claude builds into a crisp 3840x2160 (landscape) or 2160x3840 (Reels/Shorts) MP4 using only free, local tools.

## 0. Ask once (only if unclear)
- Orientation: 16:9 (YouTube/LinkedIn) or 9:16 (Reels/Shorts)?
- Length and fps (default 30 fps; 60 for fast motion/UI demos)
- Source type: Remotion project, HTML animation, or image/frame sequence

## 1. Requirements (all free)
- Node.js 18+ and ffmpeg installed locally (`ffmpeg -version` to check)
- Remotion is free for individuals and companies with up to 3 people; larger teams need a company license
- At least 8 GB RAM; 16 GB recommended for 4K

## 2. Path A - Remotion project (best quality)
1. In the composition, design at 1920x1080 (or 1080x1920) and scale up at render, OR set width/height to 3840x2160 directly.
2. Render:
```bash
npx remotion render src/index.ts MainVideo out/video-4k.mp4 \
  --scale=2 --codec=h264 --crf=18 --x264-preset=veryfast \
  --concurrency=50% --image-format=jpeg --jpeg-quality=95
```
- `--scale=2` turns a 1080p composition into 4K with sharp text and vectors
- Use `--x264-preset=slow` only when the user asks for best quality (2-3x slower)
- Low RAM: use `--concurrency=1`

## 3. Path B - HTML/canvas animation
1. Make the page deterministic: drive animation from a `window.seek(t)` or frame index, not `requestAnimationFrame` wall time.
2. Capture frames with Playwright at device scale 2:
```js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.cwd() + '/index.html');
  const fps = 30, secs = 15;
  for (let i = 0; i < fps * secs; i++) {
    await p.evaluate(t => window.seek(t), i / fps);
    await p.screenshot({ path: `frames/f${String(i).padStart(5,'0')}.png` });
  }
  await b.close();
})();
```
3. Encode (Path C).

## 4. Path C - Frames or clips to 4K MP4 with ffmpeg
```bash
ffmpeg -framerate 30 -i frames/f%05d.png -i audio.mp3 \
  -vf "scale=3840:2160:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k \
  -movflags +faststart -shortest out/video-4k.mp4
```
- Vertical: `scale=2160:3840`
- No audio: drop `-i audio.mp3`, `-c:a ...`, `-shortest`
- Smaller file for uploads: `-crf 20`; near-lossless master: `-crf 14`
- GPU (NVIDIA): `-c:v h264_nvenc -preset p5 -cq 19` (much faster)

## 5. Quality checklist
- Text at least 48px at 4K (24px at 1080p before scaling)
- Use SVG/vector assets and fonts, not small PNGs, so upscaling stays sharp
- Keep `yuv420p` and `+faststart` for YouTube/Instagram/LinkedIn compatibility
- Check one frame: `ffmpeg -ss 5 -i out/video-4k.mp4 -frames:v 1 check.png`
- Confirm: `ffprobe -v error -show_entries stream=width,height,r_frame_rate out/video-4k.mp4`

## 6. Delivery
- Give the user copy-paste-ready commands for their OS (Windows: use `^` instead of `\` for line breaks in cmd, or a single line)
- State expected render time roughly: 4K is about 4x the work of 1080p
- If the render runs in Claude's sandbox and a package is missing, say so and hand over the local commands instead of failing

## Troubleshooting
- Out of memory: lower concurrency, use jpeg frames, render in chunks (`--frames=0-299`) then join with `ffmpeg -f concat`
- Blurry text: render with scale 2 instead of upscaling a finished 1080p MP4
- Choppy motion: animation is time-based, not frame-based; switch to seek/frame driving
- Audio out of sync: set exact fps on both capture and encode

## 7. Prompt Techies Reel workflow (proven in this project)
Scripts live next to this file in `scripts/`; brand assets in `assets/` (logo, Kaushan Script font + OFL).

**Order:** narration first (its timing sets every shot) → 16:9 master → sound → brand layout → export → verify.

**Masters.** 3D: anidoodle three-core, every value set from the frame number; render at native 4K width with
`node tools/render.mjs <film> --workers 4 --scale 1.1` (2112x1188; dimensions must be even, `--scale 1.125`
fails). Realism: procedural wood/plank/plaster textures, props, practical lights, `softShadows` +
`draw3d(..., { shadows: true })`. Hand-drawn (claude-animation-base): fixed 1920x1080, `--soft-gl`, 12 fps,
one page per process, split the time range across processes and join; set `page.goto` `timeout: 0`.
Always check a one-frame-per-second contact sheet before and after a long render.

**Vertical Reel layout** — `scripts/brand.py <dir> <scale> "<TITLE>" "<TAG>"` then `scripts/reel.sh`
(1080x1920 coordinates; double for 4K):

| Element | Position |
|---|---|
| Background | dark navy gradient, soft blue glow |
| Logo icon (head only, no box) | top-right, x W-w-6, y 44 |
| Title box (white, blue underside, Big Shoulders) | centred, y 300, clear gap under the logo |
| Tag (blue pill, e.g. "30 SEC STORY") | centred, y 446 |
| Full 16:9 video ("YouTube frame") | 1040x585 at x 20, y 690, rounded 28 px, glowing ring |
| Captions (white, black outline, key words yellow/blue) | centre y 1440 (`scripts/captions.py`) |
| "Prompt Techies" (Kaushan Script, cyan→blue gradient, glow) | centred, y 1748 |
| End card | 2.5 s white card, full logo, "Follow for more AI tips", spoken end line |

Rejected by the user: cropping the wide scene, blurred side bars, an orange wordmark, a white badge behind the
logo, a title touching the logo, and an oversized blocky 3D character.

**Voice** — `scripts/voice.py lines.json outdir [voice]`: Kokoro TTS offline with studio processing.
Most natural: `af_heart`; male: `am_michael`, `am_fenrir`. English/Hindi only (no Telugu).

**Sound design that holds attention** (numpy-synthesised, licence-free): a punchy hit on frame 0,
notification pings, keyboard clicks, a riser into each reveal and an impact on it, a whoosh on every cut,
foley for actions, a success chime, ambience for the time of day, a logo sting; music follows the mood and
ducks under the voice.

**Honest limits:** upscaled 1080p is clean but not sharper (text drawn at 4K is); Instagram re-compresses to
~1080 wide; no GPU means slow software rendering — quote times from a measured frame and offer a draft first.
You cannot hear audio: ask the user to listen before posting.

## 8. One-command render script

`scripts/render4k.sh` (Windows: `scripts/render4k.ps1`):

```sh
scripts/render4k.sh --src <path> [--orientation 16x9|9x16|1x1] [--fps 30] [--quality draft|standard|master] \
                    [--gpu auto|nvidia|amd|intel|apple|none] [--duration 5] [--comp Main] [--out out/x.mp4]
```

It detects the source: a **Remotion project** (package.json with `remotion`) → `npx remotion render`; an
**HTML file** → `scripts/html2frames.mjs` (Playwright, virtual clock, deterministic frames); a **frames
folder** (png/jpg sequence) → encoded directly; a **video file** → re-encoded. Then it applies the
orientation (blurred-background pad), the quality preset and the encoder, and runs `verify.py`.

| Preset | Size | Encoder settings |
|---|---|---|
| draft | 1080p | crf 26, ultrafast — quick preview |
| standard | 4K | crf 18, veryfast |
| master | 4K | crf 14, slow, 10-bit (`yuv420p10le`) + a ProRes 422 HQ `.mov` copy |

GPU auto-detect: `nvidia-smi` → `h264_nvenc`/`hevc_nvenc`; Apple → `h264_videotoolbox`; Intel → `h264_qsv`;
AMD → `h264_amf`; otherwise `libx264`. A hardware encoder is only used if ffmpeg lists it.

## 9. Multi-platform export in one go

`scripts/export_all.sh <4k master> <outdir>` exports in parallel from one master:

| Target | Output |
|---|---|
| YouTube 4K | 3840x2160, H.264, crf 18, AAC 192k |
| Shorts / Reels / TikTok | 2160x3840 plus a 1080x1920 copy (Instagram re-compresses 4K anyway) |
| LinkedIn | 1920x1080, crf 20, ≤ 5 GB |
| X / Twitter | 1920x1080, ≤ 512 MB, bitrate cap 25M |
| Square feed | 1080x1080 |

Aspect changes use a blurred-background pad (default) or a centre crop (`CROP=1`):
`[0]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,boxblur=40[bg];[0]scale=2160:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2`

## 10. Audio polish (free)

`scripts/audio_polish.sh` subcommands:
- `loudnorm in out` — `loudnorm=I=-14:TP=-1:LRA=11` (YouTube/Spotify −14 LUFS)
- `denoise in out` — `afftdn=nf=-25`
- `duck voice music out` — music ducked under the voice with `sidechaincompress`
- `fade in out` — `afade=t=in:d=0.5` and `afade=t=out:st=<end-0.8>:d=0.8`

## 11. Free auto-captions

`scripts/autocaptions.sh <audio|video> <out.srt> [--burn video out]` uses faster-whisper or whisper.cpp
locally. Both need their model downloaded once from Hugging Face; if the network blocks it, say so and use
section 6 with the script text. Burn with
`subtitles=captions.srt:force_style='FontName=Inter,FontSize=18,Bold=1,Outline=2,Alignment=2,MarginV=120'`.
For Remotion, convert the .srt to word-level JSON for karaoke-style highlight captions. Always also deliver
the separate .srt for YouTube upload.

## 12. Visual finishing

`scripts/finish_visual.sh` subcommands:
- `watermark in logo out` — `overlay=W-w-60:H-h-60` at 80% opacity
- `sharpen in out` — `unsharp=5:5:0.6` (after any upscale)
- `grain in out` — `noise=alls=4:allf=t` (premium feel, stops gradient banding)
- `lut in brand.cube out` — `lut3d=brand.cube`
- `stitch intro main outro out` — `xfade=transition=fade:duration=0.5`
- `thumb in outdir` — sharpest scene-change frame → 1280x720 JPG + 4K PNG

## 13. Speed tricks

- Chunked parallel render: split frames into N parts (one per CPU core), render each, join with `-f concat -c copy`.
- Render cache: `render4k.sh` hashes the source + flags and skips the render if the output for that hash exists (`--force` to override).
- Preview first: offer a 10-second `--quality draft --duration 10` clip before a full 4K render.
- Remotion Lambda is NOT free: never use it unless the user asks.

## 14. Batch mode

`python scripts/batch.py jobs.json` reads `[{src, orientation, title, music, captions, quality, duration}]`,
renders each to `out/<slug>/`, mixes the music if given, burns captions if given, and prints a table
(file, resolution, duration, size, time taken).

## 15. Final verification (automatic)

`python scripts/verify.py <file> [--w W --h H --fps F --audio yes|no --platform youtube|reels|linkedin|x|square]`
runs ffprobe and fails loudly on a wrong resolution, an fps mismatch, missing audio when audio was expected,
true peak above −1 dBTP, or a file over the platform's size limit. Prints a ✅/❌ report and exits non-zero on ❌.
`render4k.sh`, `export_all.sh` and `batch.py` call it on every output.

## 16. Realism standard (every video)

Every 3D, hand-drawn, motion-graphics or AI scene follows `references/realism.md`: textured surfaces (wood grain,
plank joints, plaster, glass reflections), one real key light with cast shadows, practical lights, 4–6 real props,
contact shadows, natural voice and matched foley. Check one still at full size and a contact sheet before any
long render. For the Prompt Techies Reel, render 3D at 2112×1188 (the 4K panel is about 2080 px wide).
