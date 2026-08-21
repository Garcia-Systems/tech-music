# Lab 02 — Hear, See, and Inspect Musical Data

## Goal
Compare tempo, rhythmic placement, pitch, scales, chords, bass, and motif events without requiring notation literacy.

## Run

```bash
python - <<'PY'
from pathlib import Path
from tech_music.music import *
for bpm in (60, 90, 120, 150): print(bpm, click_positions(bpm, 4))
print("straight", step_positions([1,1,1,1], 120))
print("swing", step_positions([1,1,1,1], 120, swing=.35))
print("A pitches", [(n, midi_to_frequency(n)) for n in (57,69,81)])
notes = transpose(60, MAJOR)
render_events([NoteEvent(n, i/2, .4) for i,n in enumerate(notes)], Path("assets/part-02/c-major.wav"))
render_events([NoteEvent(n, 0, 2) for n in transpose(60, MAJOR_TRIAD)], Path("assets/part-02/c-major-triad.wav"))
PY
```

The commands generate two short, original sine-based WAV files. Generated outputs belong under `assets/part-02/` and are ignored by Git.

## Observe
1. Calculate a predicted beat interval before reading each printed list.
2. Clap straight and swung timestamps. Which positions moved?
3. Play A3, A4, and A5 safely. Compare pitch and waveform cycle density.
4. Compare a single C, C+G, C major, C minor, and C+C-sharp+G. Describe rather than prescribe an emotion.
5. Repeat a three-note motif, then change one pitch, start, duration, velocity, or octave.

Record **heard**, **seen**, **data inspected**, **change made**, and **remaining uncertainty** separately. Listening cannot validate a file header; a test cannot prove groove.
