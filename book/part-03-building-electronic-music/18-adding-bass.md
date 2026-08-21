# Chapter 18 — Adding Bass

Kick and bass often form a structural foundation because both shape low-register rhythm. They need not always coincide: this score puts each bass onset half a beat after a kick, making their relationship inspectable without introducing sidechain compression. Part II Chapter 12 supplies the pitch and register foundation.

`loop_events()` uses roots C2, C2, F2, and G2, short durations, repetition, and rests. Octave changes preserve pitch class but alter register; longer duration changes overlap and motion. Render and compare `02-drums.wav`, a bass-only filtered score, and `03-drums-bass.wav`. Change `roots`, but retain 0–127 MIDI-compatible note-number values. These generic sequencer events are not yet MIDI messages.

## Listening lab
**Objective:** separate the bass's pitch role from its rhythmic role. **Conditions:** same loop, level, and start time. **Listen for:** kick/bass alternation, root motion, and register. **Observations:** mark collisions and gaps on the aligned grid. **Reflection:** would alignment or contrast suit your intent? **Limitations:** small speakers may underrepresent bass.

## Debugging: timing or pitch?
Change one start from `2.5` to `2.25`, then restore it and change pitch 41 to 29. The first changes *when* the note happens; the second retains pitch class F but drops an octave. Use timestamps for the timing hypothesis and pitch integers/frequency for the pitch hypothesis.

## References
See the [project bibliography](../../references/bibliography.md): Butler [19] for rhythm, meter, and form in electronic dance music; Laitz [24] for music terminology; Huron [27] for expectation; Moore [28] for recorded-song layers and arrangement; and Roads [29] for computer-music sequencing and synthesis terminology. Claims here are deliberately limited to what those sources support.
