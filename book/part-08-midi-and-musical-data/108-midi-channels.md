# Chapter 108 — MIDI Channels

Traditional MIDI 1.0 channel voice messages address 16 logical channels. Many APIs number them 0–15 while user interfaces often display 1–16; this repository stores 0–15 and says so at every boundary.

| Concept | Holds/routes | Typical numbering |
|---|---|---|
| MIDI channel | channel messages toward a receiver/part | API 0–15; UI often 1–16 |
| audio channel | one signal stream, such as left or right | system-specific |
| DAW track | timeline/container with routes and processors | project-specific |

`Router({0: SINE, 1: SAW})` makes destination choice explicit. A channel does not inherently name an instrument. Sending channel 0 to a router that exposes only channel 1 produces silence in a permissive system; our educational validator instead reports `no destination`, making the wrong-channel bug visible.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
