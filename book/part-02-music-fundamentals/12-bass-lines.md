# Chapter 12 — Bass Lines

Bass is low-register musical material that can clarify harmonic roots, reinforce or counter the drums, and shape groove. **Root movement** traces chord foundations; **repetition** makes that movement legible. An **octave** doubles frequency and moves twelve MIDI semitones. A **passing note** connects more structurally important pitches, but its role depends on context.

## Build with a sequencer representation
Start with root events on beats 0, 4, 8, and 12:

```python
roots = [NoteEvent(36, 0, 1), NoteEvent(36, 4, 1),
         NoteEvent(41, 8, 1), NoteEvent(43, 12, 1)]
```

Align these with four kick attacks. Then move the last bass onset from beat 12 to 11.5, or insert MIDI 40 between 36 and 41. A useful bass line need not be busy; register, duration, rhythm, and silence are part of the design.

## Listening lab
Render four versions: drums alone (short noise-like clicks are sufficient), bass alone, both together, and both with the shifted bass onset. Level-match approximately and describe attacks, perceived momentum, gaps, and whether layers reinforce or compete. Avoid declaring one version universally better.

Bass plus drums illustrates structured coordination: two valid event lists can interact poorly if their timing was not intentional. It also foreshadows layering and mixing without teaching either in full.

## References
See the [bibliography](../../references/bibliography.md): Butler [19] on rhythmic and metrical design in electronic dance music; Laitz [24] on roots and non-chord tones; Moore [28] on arranging and register in recorded popular music.
