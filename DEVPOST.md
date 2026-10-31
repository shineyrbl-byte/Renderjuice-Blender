## Inspiration

The contest theme was **Speed**, and the obvious move is to make something go really fast. I wanted the fastest possible thing to lose anyway. The film is built like a racing ad: countdown lights, a neon tunnel, a speedometer climbing past Mach 3. The punchline undercuts all of it, because speed is relative.

I also wanted the entry to be **100% programmatic**. There are no hand-placed keyframes and no downloaded assets. One Python script builds the whole film from an empty Blender file.

## What it does

*Escape Velocity* is a 16-second animated short (1080p, 24 fps, with sound):

1. A glowing orb lines up on the start line next to its only rival, a snail.
2. Three red lights, then green. The snail inches forward and the orb launches.
3. The orb tears through a tunnel of 413 neon arches and a city skyline, going from 0 to Mach 3 in eight seconds. The camera widens, shakes, and falls behind.
4. It slams the brakes in a shower of sparks and crosses the finish line.
5. The camera swings around: the snail is already on the 1st-place podium holding the trophy. Nobody knows how.
6. The orb deflates into a sad pancake, to a sad trombone.

The whole film can be rebuilt from scratch with one command:

```bash
blender -b -P speed.py -- --render
```

## How we built it

Everything comes from `speed.py` (Blender Python API) and `audio.py` (a pure-Python synthesizer). Blender 5.2, rendered in EEVEE.

**One speed curve drives everything.** The film is built around a single velocity function in metres per frame. During launch, with \\( \tau \in [0,1] \\) as progress through the acceleration phase:

$$
v(\tau) = v_{max}\left(0.85\,\frac{e^{a\tau}-1}{e^{a}-1} + 0.15\,\min(1,\,6\tau)\right), \quad a = 3.2,\; v_{max} = 45\ \text{m/frame}
$$

The linear term is the launch kick and the exponential term is the build to top speed. Braking eases out as \\( v(u) = v_{max}(1-u)^{2.5} \\). Position is the running sum \\( s(f) = \sum v \\). Top speed is \\( 45 \times 24 \times 3.6 \approx 3888 \\) km/h, about Mach 3.1.

Every other element is derived from \\( v \\):

- **Squash and stretch:** the orb stretches by \\( 1 + 2.4\,v/v_{max} \\) and keeps its volume.
- **Camera:** chase distance, launch lag, braking catch-up, and shake ( \\( \propto (v/v_{max})^{1.5} \\) ).
- **Lens:** the field of view widens from 38 mm to 16 mm as speed increases.
- **Comet trail:** its length scales with \\( v \\).
- **Speedometer HUD:** shows km/h and Mach.
- **Soundtrack:** the engine pitch follows the same curve.
- **Set layout:** the finish line and podium are placed where the curve says the orb stops.

**Procedural world with Geometry Nodes.** Python generates point clouds with a per-point scale attribute. A Geometry Nodes tree, also built in Python, instances geometry onto them:

- 413 neon arches (a Curve Circle swept with Curve to Mesh)
- about 1,000 skyline buildings
- about 2,300 light streaks, which EEVEE motion blur turns into speed lines

**Shaders and FX:**

- **Road grid:** pure math nodes on world position.
- **Building windows:** a Brick texture driven by world coordinates. **Finish line:** a Checker texture.
- **Braking sparks:** 120 particles from a small ballistic simulation (drag, gravity, bounce) baked to keyframes.
- **Launch:** a shockwave ring.
- **Render:** EEVEE with raytraced reflections, motion blur, compositor bloom, and AgX color.

**HUD.** A frame-change handler stored inside the `.blend` writes the countdown, speedometer, and punchline. The HUD is parented to the camera and repositioned every frame to make up for the lens zoom.

**Sound.** `audio.py` synthesizes everything with no samples:

- countdown beeps
- an engine tone pitched from the speed curve
- a frequency-modulated braking screech
- a reveal ding
- a sad trombone

## Challenges we ran into

- **Making speed read on screen.** A fast object in empty space looks static. What sold it was static geometry the camera passes (arches, streaks, grid lines), motion blur, a widening lens, and shake that grows with velocity.
- **Blender API changes.** Blender 5.x moved the compositor to node groups and removed EEVEE's built-in bloom. The script detects which API is available and falls back gracefully.
- **Too much glow.** Early renders washed the frame cyan. I had to tune bloom and building emission so it still looked fast without turning to haze.
- **Landing the joke.** In the first cut the snail only appeared at the end, and a viewer asked "is it a snail running and getting first place?" Adding a line-up shot at the start, with the snail beside the orb, is what makes the ending pay off.
- **Deadline.** The whole film went from empty folder to final render in a single day.

## Accomplishments that we're proud of

- **Fully code-driven film:** no hand keyframes, no external assets, and the soundtrack is code too.
- **One equation drives the whole film:** change \\( v_{max} \\) and the camera, HUD, sound, and set layout all re-time together.
- **Thousands of procedural objects:** generated and rendered at about 3 seconds per 1080p frame on a laptop.
- **A comedic beat:** it works without any dialogue.

## What we learned

- Driving a film from one parametric curve makes iteration fast and keeps every element in sync.
- Geometry Nodes can be built entirely from Python and used as a fast instancing engine.
- In a speed piece, comedy comes from timing. The slowest beat is the payoff.
- Small tests save hours. Rendering a handful of key frames before the full render caught every framing problem early.

## What's next for Escape Velocity

- **Episode two:** a rematch where the orb tries to cheat (wormholes, rockets) and still loses to the snail.
- **Snail with personality:** more character animation, such as a smug blink or a trophy polish.
- **Parametric remixes:** expose the speed curve, colors, and track length as inputs, so anyone can generate their own race variant through the RenderJuice API.
- **Better sound:** richer layered audio and a short musical sting for the reveal.

## AI and asset disclosure

No third-party models, textures, music, or sound effects are used. The scripts were written with help from an AI coding assistant (Claude, by Anthropic). No AI image, video, or audio generators were used. Every frame is rendered by Blender and every sound is synthesized by `audio.py`.
