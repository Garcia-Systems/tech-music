# Lab 06 — From oscillator to playable synthesizer

## Goal

Use the same code to hear, visualize, explain, modify, implement, and debug a signal path. Work at a safe playback level.

## Run

```bash
python examples/part_05_synth.py
pytest tests/test_synth.py
```

The generator writes ignored, reproducible WAV/SVG artifacts to `assets/part-05/`. Confirm the printed counts and inspect file headers before playback.

## Listening matrix

Change **one independent variable per render**, give each output a new filename, and record observations rather than ratings.

| Question | Controlled comparison | Evidence to retain |
|---|---|---|
| Waveform | sine/square/saw/triangle at 220 Hz | plot, description |
| Envelope | fast/slow attack; short/long release | curve, transient observation |
| Filter | cutoff 400/1200/5000 Hz | before/after plot and peak |
| Modulation | rate .5/4/15 Hz; shallow/deep | LFO/destination ranges |
| Mix | 220+220, 220+222, 220+440 Hz | peak and beating observation |
| Additive | 1, 2, then 5 harmonics | component list and sum |
| FM | depth 5/40/200 Hz | parameter record and description |
| Patch | bass/pluck/pad/lead variants | JSON diff and in-context note |

## Capstone

Read `data/part-05-patch.json` and the note list in `render_capstone`. Trace:

**patch + note events → validation → frequencies → voices → mix → WAV**.

Copy the patch, change its role intentionally, render again, and explain which source, articulation, spectrum, or movement decision serves that role. The schema is educational, not universal.

## Completion evidence

Record exact command, sample rate, artifact names, measured peaks, and what was heard. A generated file is not proof that anyone listened to it.
