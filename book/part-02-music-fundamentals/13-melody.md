# Chapter 13 — Melody

A melody is not pitch alone. Its **contour** rises, falls, or repeats; a **step** moves to a nearby scale member and a **leap** moves farther. A short recognizable **motif** can grow into a **phrase** through repetition and variation. A **sequence** restates material at another pitch level. **Register** locates it broadly as low or high, and rhythm determines when its pitches matter.

```python
[
    {"pitch": 60, "start": 0.0, "duration": 0.5, "velocity": 90},
    {"pitch": 62, "start": 0.5, "duration": 0.5, "velocity": 90},
    {"pitch": 64, "start": 1.0, "duration": 1.0, "velocity": 90},
]
```

This event model says what, when, how long, and with what nominal intensity. It is one teaching representation—not a canonical music format—and it foreshadows MIDI and sequencer data. `NoteEvent` validates these fields; `render_events` converts beat-relative starts into seconds and audio.

## Motif experiment
Render the three events. Repeat them four beats later; transpose the repeat by two semitones to make a sequence; then alter only the last duration. Hear, see in a hand-drawn piano-roll timeline, describe the contour, inspect the records, and manipulate one field at a time.

Rules cannot guarantee a compelling melody. The data model makes decisions explicit enough to compare and debug.

## References
See the [bibliography](../../references/bibliography.md): Laitz [24] for motive, phrase, interval, and sequence terminology; Huron [27] for expectation; MIDI Association [20] for the later note/velocity connection.
