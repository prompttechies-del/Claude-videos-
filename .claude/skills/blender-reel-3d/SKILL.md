---
name: blender-reel-3d
description: Render the 3D shots of a Prompt Techies Reel in real Blender (headless, free) - voxel rooms, characters, camera moves, depth of field, glowing screens - and composite them under kinetic text. Use for any animated 3D video or 3D scene in a Reel.
---

# Blender 3D shots for Reels

Works in the cloud container with no screen and no GPU.

## Setup (once per session)
`bash .claude/skills/blender-reel-3d/scripts/setup.sh` (installs Blender 4.0 and libEGL).

## Facts measured here (4 CPUs)
- EEVEE renders a 1080x1920 frame in about 6 s; use it for every Reel shot.
- Cycles takes about 52 s a frame and this build has no denoiser (`use_denoising=False`), so keep it for single stills.
- EGL warnings at start are harmless; EEVEE still renders.
- Blender MCP needs Blender's window, which this machine lacks: script Blender directly with `blender -b -P scene.py` instead.

## Pipeline
1. Plan the shots with `prompt-techies-director` (one shot per voice line, camera always moving).
2. Build the scene in Python (`create-3d-scene`, `script-blender-automation`): blocky voxel props, emissive screens and lamps, a strong rim light, a coloured fill, fog or a dark world.
3. Animate with keyframes on the camera (push-in, orbit, dive into a screen) and on the characters (hop, squash, arms). Use Bezier easing; never linear.
4. Turn on depth of field (`camera.data.dof`, f/1.4 to 2.8) and bloom for the glow look.
5. Render the shot range to PNG with EEVEE at 1080x1920, 16-32 samples (`render-blender-output`).
6. Layer the frames under the HTML kinetic-text pass and mix sound, then output and verify with `free-4k-video-render`.

## Characters
Clawd (blue) and the helper (orange, headphones) as rounded blocks with eyes and mouth; no eyebrows, no cheek dots, no dark outline strokes. Expressions through eye size, mouth shape, squash and stretch.
