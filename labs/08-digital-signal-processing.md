# Lab 08 — Hear, See, and Debug DSP

Use low playback volume. Run `python examples/part_07_dsp.py`, open every SVG,
and inspect every WAV with `python -m tech_music.digital_audio PATH`. Predict
peak, RMS, delay onset, and dominant bin before measuring them.

Compare clean/clipped, dry/reverberated, rich/filtered, hard/soft distortion,
compressed/uncompressed, and alternate rack orders. Listening is subjective;
the numeric assertions in `pytest -q tests/test_dsp.py` are not.

## Capstone debugging

Use the broken configuration in the Part VII README. For each fault document
**Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix →
Verification**, including units at every conversion. Then restore safe gain,
milliseconds, feedback, stage order, persistent state, and sample-rate metadata.
