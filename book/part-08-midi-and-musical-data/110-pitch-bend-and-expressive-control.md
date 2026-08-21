# Chapter 110 — Pitch Bend and Expressive Control

Pitch bend is separate from the integer note number. MIDI 1.0 communicates a high-resolution bend position around a center; the receiver also needs a configured bend range. The message does **not** impose one universal semitone range.

`bend_frequency(note, bend, range_semitones)` normalizes the signed teaching representation (`−8192..8191`) and applies the explicitly supplied range. `pitch-bend.svg` shows note 69 under a configured ±2-semitone range; `pitch-bend-steps.wav` is a stepped listening approximation rather than a claim of smooth production bend.

**Debugging.** If sender expects ±12 and receiver uses ±2, the same maximum value yields an octave versus a whole tone. Inspect both raw bend value and receiver configuration, then test center and endpoints.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
