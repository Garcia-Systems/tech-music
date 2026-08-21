# Chapter 224 — Yoshimi in the System

> **Status:** reviewed educational model. Hardware behavior is not probed.

Yoshimi is the software-synthesizer case study: MIDI/event input controls a synthesis engine whose digital audio outputs enter an audio-routing system, a DAW, or hardware path.

```text
MIDI/event → Yoshimi synthesis → audio outputs → router/DAW → device
```
Patch, part/channel, MIDI input, and audio output are separate boundaries. Feature/UI claims depend on installed version; the official user guide is the revalidation target. Revisit [synthesis](../part-05-synthesizers/README.md).

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
