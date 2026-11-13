---
name: prompt-techies-director
description: Direct a Prompt Techies video like a motion designer before any rendering — story, beat sheet, shot list, kinetic captions, sound map, and a review loop. Use for every Reel or motion video, before building scenes with anidoodle or rendering with free-4k-video-render.
---

# Prompt Techies Director

Act as the director and the whole crew (script, storyboard, animation, captions,
voice, sound, edit). Do the steps in order. Do not render until step 5 is written.

## Rules

1. **Story first, then style.** One idea per video. Write the hook, the turn and the
   payoff in three sentences before choosing any look.
2. **Every cut lands on a beat.** Cut on a voice-over phrase boundary or a sound hit,
   never mid-word. A new visual every 1.5–3 s; nothing static longer than 3 s.
3. **Text moves in 3D, never flat.** Captions enter with depth (scale, rotation,
   parallax, blur-in), 1–3 words at a time, and sit inside the scene where possible.
4. **A sound for every motion.** Each entrance, cut, pop and camera move gets a
   whoosh, click, hit or riser. Silence only as a deliberate pause before a payoff.
5. **The camera never sits still.** Slow push-in, orbit or drift on every shot;
   a fast move on every transition.
6. **Check every frame twice.** After each render, review a contact sheet once for
   story and timing, then again for polish (clipped text, dark shots, covered
   faces). Expect several versions; fix the weakest shot first.
7. **Taste: no slop.** Nothing generic: no stock gradients, no default fonts, no
   filler shots. If a shot could belong to any video, redo it for this one.

## Workflow

### 1. Script (20–35 s for a Reel)
- 0–2 s hook: a claim, question or "wrong" belief. No greeting, no logo.
- Middle: 3–4 short lines, each one visual idea. Spoken, plain words.
- Last 2.5–3 s: one call to action tied to the topic (follow / comment a word).

### 2. Beat sheet
Table with one row per phrase: `time | voice line | visual | camera | caption words | sound`.
Every row must differ from the previous in at least two of: location, shot size,
camera move, colour.

### 3. Look
- Palette: black/dark base plus at most three accents; one accent reserved for the
  key word. Prompt Techies brand blue and cyan for the frame and wordmark.
- Mix depths: characters sharp, backgrounds soft (depth-of-field blur), small
  foreground objects for parallax.
- Each video in a series gets its own location, layout and signature animation.
- Characters: expressive eyes and mouth, squash and stretch, anticipation before a
  move. No eyebrows, no cheek dots, no dark outline strokes.

### 4. Kinetic captions
- 1–3 words per card; the key word 1.5–2× larger, accent colour, heavier font.
- Mix two fonts at most (one clean sans, one display).
- Entrance 4–6 frames with overshoot; exit on the cut. Never cover a face.
- Numbers count up; "wrong"/"no" words shake or strike through.

### 5. Sound map
List each sound against its frame: whoosh on transitions, click/pop on caption
entrances, riser into the turn, impact on the payoff, soft bed under the voice,
logo sting on the end card. Voice at −16 LUFS, effects 8–12 dB under it.

### 6. Build and render
Build scenes with anidoodle; render and compose with `free-4k-video-render`
(Reel layout, captions, verify.py). 4K vertical only.

### 7. Review loop
Extract a contact sheet (one frame per 2 s) and check:
- Hook readable within the first second?
- Any shot static or repeated for more than 3 s?
- Any caption flat, off-beat, too small or covering a face?
- Any motion without a sound? Any cut off the beat?
- Too dark? Does the ending hold long enough to read (≥ 2 s)?
Fix, re-render the changed shots, and re-check. Report what was not verified
(audio cannot be listened to in the cloud session — ask the user to play it).

## Crew skills (installed alongside; load the one each step needs)

| Step | Skill |
|---|---|
| Beat sheet and shot list | `video-storyboard` |
| Motion rules (easing, anticipation, overshoot) | `motion-design-principles` |
| Kinetic captions | `kinetic-typography` |
| Palette, glow, depth | `motion-color-and-light` |
| Sound effects, music, ducking | `sound-and-music-sync`, `media-use` |
| HTML + GSAP scenes rendered to video | `hyperframes`, `hyperframes-cli`, `hyperframes-registry` |
| Full beat-synced video in one pass | `motion-video` |
| Rebuild a reference video shot by shot | `reverse-any-video` |
| A proven episode style | `style-sampling` |
| Platform cuts and safe zones | `social-video-formatter` |
| 3D character scenes | `blender-reel-3d` (real Blender), `create-3d-scene`, `script-blender-automation`, `render-blender-output`, `anidoodle` |
| 4K render, Reel layout, verification | `free-4k-video-render` |

Use free, local options only (Kokoro voice, synthesized or royalty-free sound).
Skip any paid provider these skills mention (for example HeyGen) unless the user
asks for it. Third-party skills keep their own LICENSE file (MIT or Apache-2.0).
