---
name: cinematic-shorts
description: Make a cinematic, ultra-realistic vertical short (9:16 reel) from AI-generated photoreal images and clips, with voice-over, music and titles. Use when asked for a "cinematic short", "realistic reel", "ultra-realistic video", or any reel that should look like film footage rather than flat motion graphics.
---

# Cinematic shorts

Produces a 1080x1920 MP4 that looks like film: photoreal AI stills, animated into
clips or moved with a slow camera, graded, letterboxed, with voice, music and titles.
Do not use flat UI mock-ups, emoji, pixel art or cartoon graphics in this style.

## Requirements

The session's environment must allow these hosts, each with the user's Hugging Face
token saved as a network secret (the proxy injects it; never ask for it in chat):

- `mcp-tools-flux-1-krea-dev.hf.space` (photoreal images)
- `zerogpu-aoti-wan2-2-fp8da-aoti-faster.hf.space` (image to video)

`github.com` release downloads must be reachable for the voice model.
Tools: `pip install gradio_client kokoro-onnx soundfile numpy`, and `ffmpeg`.

## Steps

1. **Script.** 5-7 shots, 25-40 seconds. One line of narration per shot, written
   for the ear. Save as `shots.json`: `[{"id","image_prompt","motion_prompt","line","title"}]`.
2. **Images.** `python scripts/gen_image.py shots.json out/`. Write every
   `image_prompt` with the rules under "Realism" below.
3. **Look at every image** before spending video quota. Regenerate any with warped
   hands or faces, garbled text or a plastic look.
4. **Motion.** `python scripts/gen_clip.py shots.json out/` animates each still
   (about 5 seconds each). It stops cleanly when the daily quota runs out.
5. **Voice.** `python scripts/tts.py shots.json out/` (Kokoro, runs offline on CPU).
6. **Edit.** `python scripts/edit.py shots.json out/ final.mp4`. Shots without a
   clip fall back to a slow push-in on the still, so a reel can still be finished
   when the quota is spent. Applies grade, grain, letterbox bars, crossfades,
   lower-third titles, voice and a music bed.
7. **Check.** Extract a contact sheet with ffmpeg and look at it before sending.

## Realism

- Describe it as a photograph or film frame, never as "art" or "illustration".
- Name the camera and lens: "shot on ARRI Alexa, 35mm anamorphic" or "85mm f/1.4".
- Name the light: golden hour, overcast soft light, practical lamps, rim light, haze.
- Add texture: skin pores, dust, rain on glass, worn metal, film grain, shallow depth of field.
- One subject and one action per shot. Avoid crowds, hands in close-up and readable text.
- Keep one palette and one time of day across the reel so the shots cut together.
- Motion prompts describe camera movement and one subject movement: "slow dolly in,
  hair moves in the wind". Fast or complex action breaks realism.
- Always generate at 576x1024 (9:16). The edit upscales to 1080x1920.

## Limits to tell the user

- The free Hugging Face quota covers only about three 5-second clips a day; it resets
  after 24 hours. Images use the same quota.
- Clips are generated at 480x832 and upscaled, so they are slightly soft.
- The voice model speaks English and Hindi, not Telugu.
- Real people, brands and copyrighted characters must not be generated.
