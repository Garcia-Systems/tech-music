# Lab: Generate and verify a waveform

## Objective
Generate A4 as samples, a plot, and playable PCM WAV; then verify rather than merely trust it.

## Prerequisites
Read [Generating a Waveform with Code](../book/part-06-digital-audio/59-frequency-amplitude-and-phase.md); know how to activate the project virtual environment.

## Required software
Python 3.10+ and project dependencies from `requirements.txt`; a local image viewer and optional audio player.

## Relevant chapter
Part VI, Chapter 3.

## Files used
`src/tech_music/waveform.py`, `tests/test_waveform.py`, and generated files below `assets/`.

## Starting state
Run from repository root after installation. Generated outputs need not already exist.

## Commands to run
```bash
python -m tech_music.waveform
pytest tests/test_waveform.py
```

## Expected output
The program reports 44,100 samples, an estimate near 440 Hz, and two output paths. Five tests pass.

## Listening instructions
Reduce monitoring volume, play `assets/audio/a4-sine.wav`, and note duration, steadiness, and timbre.

## Visual inspection
Open `assets/waveforms/a4-sine.svg`; count about 4.4 cycles in 10 ms and verify ±0.5 bounds.

## Debugging challenge
Run measurements against `examples/incorrect_waveform.py` and follow the chapter's investigation without first reading the solution.

## Verification procedure
Use the test command, inspect WAV metadata reported by the test implementation, and reconcile heard/seen evidence.

## Extension challenge
Generate octave-related frequencies in `/tmp` and compare their cycle counts.

## Cleanup/reset
Delete generated ignored files with `rm -f assets/audio/a4-sine.wav assets/waveforms/a4-sine.svg`; rerun the first command to reproduce them.
