"""Procedural soundtrack for ESCAPE VELOCITY (stdlib only).
Uses the same speed curve as speed.py so engine pitch follows the orb exactly."""
import math, random, struct, wave, os

SR = 44100
FPS = 24
F_END, F_LAUNCH, F_TOP, F_STOP, F_REVEAL, F_SAD = 384, 66, 270, 300, 306, 352
VMAX = 45.0


def vel(fr):
    if F_LAUNCH <= fr <= F_TOP:
        tau = (fr - F_LAUNCH) / (F_TOP - F_LAUNCH)
        a = 3.2
        return VMAX * (0.85 * (math.exp(a * tau) - 1) / (math.exp(a) - 1) + 0.15 * min(1.0, tau * 6))
    if F_TOP < fr <= F_STOP:
        return VMAX * (1 - (fr - F_TOP) / (F_STOP - F_TOP)) ** 2.5
    return 0.0


n = int(SR * F_END / FPS)
buf = [0.0] * n
random.seed(3)


def add_tone(t0, dur, freq, amp, decay=6.0, harmonics=(1.0,), vib=0.0):
    i0 = int(t0 * SR)
    for i in range(int(dur * SR)):
        if i0 + i >= n:
            break
        t = i / SR
        f = freq * (1 + vib * math.sin(2 * math.pi * 5.5 * t))
        env = min(1.0, t * 200) * math.exp(-decay * t)
        s = sum(h * math.sin(2 * math.pi * f * (k + 1) * t) for k, h in enumerate(harmonics))
        buf[i0 + i] += amp * env * s


# countdown beeps
for fr in (12, 30, 48):
    add_tone(fr / FPS, 0.18, 660, 0.3, decay=8)
add_tone(60 / FPS, 0.6, 1320, 0.3, decay=4)

# engine: phase-accumulated buzzy tone whose pitch tracks speed, plus wind noise
phase = 0.0
lp = 0.0
for i in range(int(F_LAUNCH / FPS * SR) - 2000, int((F_STOP + 6) / FPS * SR)):
    fr = i / SR * FPS
    k = vel(int(fr)) / VMAX + (vel(int(fr) + 1) - vel(int(fr))) / VMAX * (fr - int(fr))
    rev = 0.15 if fr < F_LAUNCH else 0.0
    f = 55 + 820 * (k + rev) ** 0.8
    phase += 2 * math.pi * f / SR
    tone = math.sin(phase) + 0.5 * math.sin(2 * phase) + 0.25 * math.sin(3 * phase + 0.3)
    lp += (random.uniform(-1, 1) - lp) * (0.05 + 0.4 * k)
    amp = 0.12 + 0.18 * k
    if fr > F_TOP:
        amp *= max(0.0, 1 - (fr - F_TOP) / (F_STOP + 6 - F_TOP))
    buf[i] += amp * tone * 0.5 + (0.35 * k) * lp

# braking screech
for i in range(int(F_TOP / FPS * SR), int(F_STOP / FPS * SR)):
    t = i / SR - F_TOP / FPS
    u = t / ((F_STOP - F_TOP) / FPS)
    f = 2600 - 900 * u
    s = math.sin(2 * math.pi * f * t + 3 * math.sin(2 * math.pi * 37 * t))
    buf[i] += 0.16 * (1 - u) * (s + 0.3 * random.uniform(-1, 1))

# reveal ding
add_tone((F_REVEAL + 13) / FPS, 1.6, 1568, 0.25, decay=2.5, harmonics=(1.0, 0.3, 0.12))

# sad trombone: wah wah wah waaaah
t0 = (F_SAD - 6) / FPS
for j, (note, dur) in enumerate(((311.1, 0.3), (293.7, 0.3), (277.2, 0.3), (261.6, 0.95))):
    add_tone(t0, dur + 0.05, note, 0.22, decay=0.8 if j == 3 else 2.0,
             harmonics=(1.0, 0.6, 0.35, 0.2, 0.1), vib=0.012 if j == 3 else 0.0)
    t0 += dur

peak = max(abs(v) for v in buf) or 1.0
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soundtrack.wav')
with wave.open(out, 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(32000 * v / peak * 0.9)) for v in buf))
print('wrote', out)
