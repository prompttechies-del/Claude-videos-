# Realism standard (applies to every video)

Use this for every 3D, hand-drawn, motion-graphics or AI-generated scene. Check it before any long render.

## Surfaces
- Wood: grain plus small tonal variation, never a flat colour. Planks: staggered joints, slight tone change per board.
- Walls: plaster with fine noise, a skirting board at the floor, a faint light falloff from the window.
- Glass: a soft reflection, a city or sky behind it, never a flat blue square.
- Fabric and paper: matte, slightly rough. Metal: a satin or glossy highlight with a darker edge.
- Screens: show content (code lines, a UI), not a blank colour.

## Light
- One key light with real cast shadows (`softShadows` + `draw3d(..., { shadows: true })`), plus a fill and a rim.
- Practical lights where a real one would be: desk lamp, screen glow, window light, a warm glow near the lamp.
- Dawn scenes warm up over time; night scenes keep cool blue and small warm points.
- Contact shadows under every object and character so nothing floats.

## Props and set dressing
- Add 4–6 small real objects: a lamp, a mug, a plant, picture frames, papers with edges, a book.
- Spread them so the frame has depth: foreground item, midground subject, background wall detail.

## Characters
- Soft materials with a little sheen, subtle edge highlights, shadows on the floor.
- Eyes with a catchlight. Faces move on blinks and small head turns, never freeze.

## Motion
- Ease in and out. Add a small secondary motion (a settle, a sway, a breath) on every held pose.
- Camera: slow drift or a planned push. Never a dead static frame for more than about one second.

## Sound (for the same realism)
- Voice: a natural narrator voice (Kokoro `af_heart` by default), with EQ, light compression and a small room echo.
- Foley matched to the action: paper, keys, a mug set down, the spanner.
- Ambience for the place and time (room tone at night, birds at dawn).

## Render size
- Native width for the layout: the 4K Reel shows a 16:9 panel about 2080 px wide, so render 2112×1188 (even dimensions).
- 3840×2160 full frame only when the user asks for a 16:9 4K upload; it takes roughly four times longer.

## Quick check before a long render
1. One still at the hardest frame, looked at full size.
2. A contact sheet of about 8 frames across the whole video.
3. Ask: does any surface look flat, any object float, any light come from nowhere?
