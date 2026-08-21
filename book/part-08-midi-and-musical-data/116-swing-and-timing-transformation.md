# Chapter 116 — Swing and Timing Transformation

Swing can be modeled as a timing transformation on selected subdivisions, but there is no single universal swing formula. Our educational function leaves even subdivisions straight and delays odd ones to two-thirds through each pair: a simple 2:1 long–short model.

`straight.wav` and `swung.wav` use the same pitches and synth. `swing.svg` plots the original and transformed tick positions. The function intentionally accepts an explicit amount from 0.5 (straight) to less than 1. It does not claim to reproduce a particular musician, DAW groove template, dynamics, or articulation.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
