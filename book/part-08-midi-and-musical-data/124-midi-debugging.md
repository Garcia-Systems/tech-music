# Chapter 124 — MIDI Debugging

Use **Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix → Verification** for every case.

| Symptom | Evidence / likely boundary | Root cause and verification |
|---|---|---|
| stuck note | active table remains populated | missing note-off; add pair and assert empty state |
| silence | event log exists, synth receives none | wrong channel/route; test destination |
| wrong pitch | note and measured frequency disagree | conversion/off-by-octave; test 69→440 Hz |
| wrong timing | ticks appear as huge seconds | unit confusion; test ticks→beats→seconds→samples |
| wrong expression | CC arrives, parameter does not change | mapping mismatch; inspect route table |
| wrong instrument | correct event, unexpected patch | program/route configuration; log selected patch |
| bad retrigger | simultaneous lifecycle log reversed | ordering policy; assert note-off before note-on |

The [broken capstone exercise](../../exercises/part-08-capstone-debugging.md) combines these faults. Use event inspection, calculations with units, scheduler logs, piano roll, synth state, and tests; do not jump directly to changing DSP.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
