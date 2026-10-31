## Inspiration

The contest theme was **Speed**, and the obvious move is to make something go really fast. I wanted the fastest possible thing to lose anyway. The film is built like a racing ad: countdown lights, a neon tunnel, a speedometer climbing past Mach 3. The punchline undercuts all of it. The orb lines up next to a snail, blasts off, brakes in a shower of sparks, and finds the snail already on the winner's podium holding the trophy. Nobody knows how.

Speed is relative.

I also wanted the entry to be **100% programmatic**. There are no hand-placed keyframes and no downloaded assets. One Python script builds the whole film from an empty Blender file.

## How I built it

Everything comes from `speed.py`, run headless with `blender -b -P speed.py -- --render`.

### One speed curve drives everything

The film is built around a single velocity function \\( v(f) \\), in metres per frame. During launch, with \\( \tau \in [0,1] \\) as progress through the acceleration phase:

$$
v(\tau) = v_{max}\left(0.85\,\frac{e^{a\tau}-1}{e^{a}-1} + 0.15\,\min(1,\,6\tau)\right), \quad a = 3.2,\; v_{max} = 45\ \text{m/frame}
$$

The linear term is the launch "kick" and the exponential term is the build to top speed. Braking eases out as \\( v(u) = v_{max}(1-u)^{2.5} \\). Position is the running sum \\( s(f) = \sum v \\). At 24 fps the top speed is \\( 45 \times 24 \times 3.6 \approx 3888 \\) km/h, about Mach 3.1.

Every other element is a function of \\( v \\):

- **Squash and stretch:** the orb stretches by \\( 1 + 2.4\,v/v_{max} \\) along its motion and keeps its volume.
- **Camera:** chase distance, launch lag, braking catch-up, and shake amplitude ( \\( \propto (v/v_{max})^{1.5} \\) ).
- **Lens:** the field of view widens from 38 mm to 16 mm as speed increases, so the world rushes outward.
- **Comet trail:** its length scales with \\( v \\).
- **Speedometer HUD:** shows km/h and Mach.
- **Soundtrack:** the engine pitch follows the same curve.
- **Set layout:** the finish line and podium are placed where the curve says the orb stops.

### Procedural world with Geometry Nodes

Python generates point clouds and writes a per-point `bscale` attribute. A Geometry Nodes tree, also built in Python, instances geometry onto those points:

- **413 neon arches:** a Curve Circle swept with Curve to Mesh, rotated upright and half-buried in the road.
- **About 1,000 skyline buildings:** cubes scaled per point, in two depth layers.
- **About 2,300 light streaks:** static dashes that EEVEE motion blur turns into speed lines.

### Shaders, FX and HUD

- **Road grid:** pure math nodes on world position (`fract`, `abs`, `less than`), with no textures.
- **Building windows:** a Brick texture driven by world coordinates.
- **Finish line:** a Checker texture. **Trail:** an additive gradient.
- **Braking sparks:** 120 particles from a small ballistic simulation (drag, gravity, bounce) baked to keyframes. A shockwave ring fires at launch.
- **HUD:** a frame-change handler stored inside the `.blend` writes the countdown, speedometer, and punchline every frame. The HUD is parented to the camera and repositioned per frame to make up for the lens zoom.
- **Render:** EEVEE with raytraced reflections, motion blur, compositor bloom, and AgX color.

### Sound

`audio.py` is a pure-Python synthesizer with no samples or libraries:

- countdown beeps
- an engine tone pitched from the speed curve
- a frequency-modulated braking screech
- a reveal "ding"
- a sad trombone

## Challenges

- **Making speed read on screen.** A fast object in empty space looks static. What sold it was static geometry the camera passes (arches, streaks, grid lines), motion blur, a widening lens, and shake that grows with velocity.
- **Blender API changes.** Blender 5.x moved the compositor to node groups and removed EEVEE's built-in bloom. The script detects which API is available and falls back gracefully.
- **Too much glow.** The first renders washed the whole frame cyan. I had to tune bloom strength and building emission so it still looked fast without turning to haze.
- **Landing the joke.** In the first cut the snail only appeared at the end, and viewers asked "wait, did the snail run?" Adding the line-up shot at the start, with the snail beside the orb, is what makes the ending pay off.

## What I learned

- Driving a whole film from one parametric curve makes iteration easy. Changing \\( v_{max} \\) re-times the camera, HUD, sound, and set layout together.
- Geometry Nodes can be built completely from Python and used as a fast instancing engine for thousands of objects.
- In a speed piece, comedy comes from timing. The slowest beat in the film is the payoff.

## AI and asset disclosure

No third-party models, textures, music, or sound effects are used. The scripts were written with help from an AI coding assistant (Claude, by Anthropic). No AI image, video, or audio generators were used. Every frame is rendered by Blender and every sound is synthesized by `audio.py`.
