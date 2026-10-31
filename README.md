# Renderjuice-Blender: ESCAPE VELOCITY
Avisha Srivastava

▶ **Watch:** https://youtu.be/HSAlY_cOA3o

This is a 16-second, fully procedural Blender animation about **Speed**, made for the RenderJuice Blender Animation & Programmatic Rendering Contest.

A glowing orb launches through a neon tunnel, reaches Mach 3, and brakes in a shower of sparks. It crosses the finish line and finds a snail already on the 1st-place podium.

## Build it yourself

```bash
python3 audio.py                                              # soundtrack.wav
blender -b -P speed.py -- --render --res 1920x1080 --samples 24   # frames/
ffmpeg -framerate 24 -i frames/f_%04d.png -i soundtrack.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -shortest escape_velocity.mp4
```

Other modes:
- `--still 30,200,384` renders test frames.
- `--wip` renders clay "work in progress" images.

Tested on Blender 5.2.3.

See [SUBMISSION.md](SUBMISSION.md) for the description, workflow notes, and AI disclosure.
