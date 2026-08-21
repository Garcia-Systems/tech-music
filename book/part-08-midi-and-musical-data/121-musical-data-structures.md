# Chapter 121 — Musical Data Structures

Music software can store event objects, ordered lists, tracks, clips, patterns, graphs, tempo maps, and automation curves. MIDI is important interchange/control technology, but an application need not use raw MIDI messages as its internal model for every musical idea.

A useful schema identifies type, timestamp and unit, payload, channel/destination, track, and a stable ordering field. Serialization preserves it; IDs connect edits; validation protects boundaries; ordering makes output reproducible. `MidiEvent` is a frozen teaching record. Its tick time is explicit, but duration is intentionally expressed by a paired note-off, illustrating translation between a convenient clip model and message lifecycle.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
