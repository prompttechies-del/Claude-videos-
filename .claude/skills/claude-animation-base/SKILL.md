---
name: claude-animation-base
description: Hand-drawn character animation in p5.js and p5.brush (brush strokes, flat 2D, boiling linework) using the Clawd character kit by John Heibel. Use when asked for a hand-drawn, painterly or character-driven animated video, a mascot animation, or "an animation like the P(doom) music video".
---

# Claude Animation Base

This folder is a copy of https://github.com/JohnHeibel/ClaudeAnimationBase (MIT,
commit `0ac8bf2`). It was a starter kit, not a packaged skill; this file wraps it.

## How to use

1. Read `ANIMATION_GUIDE.md` in this folder first. It holds the rules, the workflow
   and the full API. Follow it: storyboard, build shot by shot, render contact
   sheets to check the work, then write the MP4.
2. Copy this folder to a working directory, then put the new video in `src/scenes/`
   (`src/scenes/demo.js` is the example).
3. Render: `npm install`, then `node render.mjs --clip --out=out/video.mp4`.
   Needs Node.js, Chrome or Chromium, and ffmpeg.

## Notes for cloud sessions

- There is no GPU here: add `--soft-gl`. Watercolour fills then take seconds per
  frame, so avoid them or keep clips short.
- Pass `--chrome=/opt/pw-browsers/chromium` if Chrome is not found.
- The guide's house rules include no on-screen text; add titles and captions in a
  separate edit step if the reel needs them.

## Realism

Follow `../free-4k-video-render/references/realism.md`: keep the hand-drawn look, but add believable surface texture, light direction and contact shadows, and natural narration with matched foley.
