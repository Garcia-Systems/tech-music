# Chapter 10 — Scales and Keys

A **scale** is an ordered pitch collection. Its point of reference is the **tonic**; a **key** is a broader tonal context in which pitches and harmonies relate to a tonic. A **scale degree** numbers a member relative to that tonic. A chromatic scale uses every semitone; major and natural minor select different interval patterns. **Octave equivalence** means notes separated by octaves often share a note name and pitch-class role, although they remain different pitches and frequencies.

```text
C major names:     C  D  E  F  G  A  B  C
semitone offsets:  0  2  4  5  7  9 11 12
MIDI from C4:     60 62 64 65 67 69 71 72
```

On a piano roll, vertical position is pitch and horizontal position time; the list above describes a rising diagonal when played sequentially. Each MIDI number can be converted to frequency with Chapter 9's function.

## Executable transformation
`transpose(60, MAJOR)` implements **root + interval pattern → notes**. Try roots 60 and 62, then replace `MAJOR` with `NATURAL_MINOR`. The function is reusable because the pattern contains relative distances rather than fixed notes. Export the result as consecutive `NoteEvent` values with `render_events`.

A pattern is a pedagogical representation, not a universal definition of musical culture or tuning. It deliberately supports later algorithmic composition without surveying every scale.

## Check and connection
Assert that C major yields `[60,62,64,65,67,69,71,72]`. A scale-membership check can catch an unintended note, but cannot decide whether a deliberate chromatic note is artistically wrong.

## References
See the [bibliography](../../references/bibliography.md): Laitz [24] for scales, keys, and scale degrees; Sethares [26] for tuning systems; MIDI Association [20] for note-number representation.
