# Chapter 114 — Piano Rolls

A piano roll places time on the horizontal axis and pitch on the vertical axis; a block's length represents note duration. It is an interface/visual representation, **not MIDI itself**. The same event list can appear as messages, a table, notation, JSON, a piano roll, or scheduled seconds.

`piano-roll.svg` is generated from the sequencer phrase. The current dependency-free plot marks onsets; inspect paired note-off ticks for lengths. Compare the JSON and MIDI artifact: representation changes while the intended phrase remains related. This reinforces the Part II distinction between music concepts and data models.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
