# Chapter 122 — Event Ordering and Scheduling

Events can share a timestamp. The capstone policy is `(tick, type priority, track, source order)`: program changes, CC, pitch bend, note-off, then note-on. This allows setup before attack and releases an old same-pitch voice before retriggering. It is an educational policy, not a universal protocol mandate.

`schedule` produces identical results even when its input iterable is reversed because the explicit keys decide ties. **Debugging:** if note-on precedes its same-time note-off, a receiver keyed only by channel/note can immediately stop the new voice. Log the sorted event tuple and test the collision directly.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
