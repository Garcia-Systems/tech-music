# Lab 07 — Inspect, Resample, and Break Digital Audio

Use low playback volume. Run `python examples/part_06_digital_audio.py`, then
inspect each WAV with `python -m tech_music.digital_audio PATH`. Record rate,
channels, frames, duration, representation, peak, and data bytes.

Compare the correct and wrong-metadata tones and calculate their duration/pitch
ratios. Compare correct, four-bit-grid, clipped, and stereo files. Verify
`sample_values = frames × channels`. Open all 13 SVGs and calculate Nyquist before
interpreting aliasing.

## Debug challenge

A 48 kHz generator is tagged 44.1 kHz, float-to-PCM scaling uses 128 rather than
32767, and stereo is treated as mono. For each use **Symptom → Measurements →
Hypotheses → Investigation → Root Cause → Fix → Verification**. Write units beside
every number. Then compare the [solution](../solutions/part-06-capstone-debugging.md).

Artifacts are reproducible and git-ignored; remove `assets/part-06` if desired.
