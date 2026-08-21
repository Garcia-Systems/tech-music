# Lab 09 — MIDI, Events, and the Mini Sequencer

Run `python examples/part_08_midi.py`. Inspect `phrase-events.json`, reload
`phrase.mid` with `read_midi_file`, open every SVG, and inspect each WAV with
`python -m tech_music.digital_audio PATH`. Use low playback volume.

1. Trace note 60 through validation, ticks, seconds, routing, synthesis, and WAV.
2. Compare velocity, pitch-bend steps, quantized/unquantized, straight/swung,
   controller amplitude, and the same events rendered with two patches.
3. Change PPQ while preserving musical positions. Write every intermediate unit.
4. Route channel 0 to sine and channel 1 to saw; confirm channel is neither a DAW
   track nor an audio channel.
5. Add a CC mapping explicitly; never assume receiver behavior.
6. Read Chapter 118's SMF subset warning before supplying any external file.

## Capstone

Extend the original phrase by one track and one tempo change. Validate it, inspect
the deterministic schedule, plot its piano roll, render it, save/reload the
supported SMF subset, and assert the intended duration. Explain which artifact is
musical structure, event data, MIDI-file serialization, and audio signal.

## Debugging

Complete the [broken-sequence exercise](../exercises/part-08-capstone-debugging.md)
using **Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix →
Verification** for every fault.
