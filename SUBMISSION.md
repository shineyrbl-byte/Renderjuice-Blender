# ESCAPE VELOCITY — RenderJuice "Speed" contest entry

**Name / team:** Avisha Srivastava
**Length:** 16 seconds, 1920×1080, 24 fps, with sound
**Categories:** Best Procedural & Programmatic Animation, Funniest Animation, Best Motion Design

## Short description (interpretation of Speed)

A tiny glowing orb lines up for the race of its life, next to its only rival: a snail. Three red lights, one green. The snail inches off the line, and the orb launches through a neon tunnel of arches and a city skyline. It goes from 0 to Mach 3 in eight seconds while the camera widens, shakes, and falls behind. It slams the brakes in a shower of sparks, crosses the finish line, and turns to celebrate. The snail is already on the 1st-place podium holding the trophy. Nobody knows how. The orb deflates.

Speed is relative.

## Workflow notes (procedural / programmatic)

The whole film comes from one Blender Python script (`speed.py`) with no hand-placed keyframes. A second script (`audio.py`) synthesises the soundtrack. Run `blender -b -P speed.py -- --render` to rebuild the scene and render every frame from scratch.

What the code controls:

- **Speed curve as the single source of truth.** A launch kick plus exponential acceleration and an eased braking curve give per-frame velocity. Everything else is derived from it:
  - orb position
  - squash-and-stretch (the orb stretches with velocity)
  - comet-trail length
  - camera distance and lag
  - lens zoom (the field of view widens with speed)
  - camera-shake amplitude
  - the speedometer HUD (km/h and Mach)
  - the engine pitch in the soundtrack

  The finish line and podium are placed where the curve says the orb comes to rest.
- **Geometry Nodes instancing.** Python builds point clouds and stores a per-point scale attribute. A Geometry Nodes tree, also built in Python, instances geometry on those points: 413 neon arches (a Curve Circle swept with Curve to Mesh), about 1,000 skyline buildings, and about 2,300 light streaks. EEVEE motion blur turns the static streaks into speed lines.
- **Procedural shaders.** The road grid is math nodes on world position. Building windows use a Brick texture driven by position, the finish line uses a Checker texture, and the trail uses an additive gradient.
- **Particle FX.** 120 braking sparks come from a small ballistic simulation (drag, gravity, bounce) baked to keyframes. A shockwave ring fires at launch.
- **Camera rig.** A scripted chase cam with launch lag and braking catch-up, then an orbit move for the reveal. The HUD is parented to the camera and repositioned every frame to make up for the zoom.
- **HUD.** A frame-change handler (stored inside the .blend as `hud_driver.py`) writes the speedometer, the countdown, and the punchline text.
- **Sound.** `audio.py` is a pure-Python synth: countdown beeps, an engine tone whose pitch follows the same speed curve, a braking screech, a reveal "ding", and a sad trombone.
- **Render.** EEVEE with raytracing, motion blur, and compositor bloom (all set by the script). AgX color management. Encoded with ffmpeg.

## AI and third-party asset disclosure

- No third-party models, textures, HDRIs, music, or sound effects are used. All geometry, materials, motion, and audio are generated procedurally by the scripts.
- The scripts were written with help from an AI coding assistant (Claude, by Anthropic). No AI image, video, or audio generators were used. Every pixel is rendered by Blender, and every sample comes from the synth script.
- Font: Blender's built-in default font.

## Files

- `escape_velocity.mp4` is the final animation.
- `wip/wip_corridor.png` and `wip/wip_finish.png` are Blender work-in-progress clay renders of the procedural set.
- `speed.py`, `audio.py`, and `escape_velocity.blend` are the source.
