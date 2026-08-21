# Chapter 111 — Aftertouch and Other Performance Data

MIDI can describe how a performance evolves after attack. **Channel pressure** supplies one pressure value for a channel; **polyphonic key pressure** associates pressure with an individual note. Other controls and newer MIDI facilities can carry further expression.

These messages still do not contain a sound. A receiver may map pressure to vibrato, filter, loudness, or nothing. Our capstone omits pressure processing to keep scope honest: adding it requires an event schema, validation, an explicit mapping, and synth behavior—not merely a label. This illustrates that MIDI conveys more than “which note and when” without pretending to cover every message.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
