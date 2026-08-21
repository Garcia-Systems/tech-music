# Chapter 223 — Ardour in the System

> **Status:** reviewed educational model. Hardware behavior is not probed.

Ardour is the DAW case study: inputs enter tracks, processors transform streams, buses combine routes, the master feeds the selected audio system/device, and export writes a file. MIDI tracks may drive instruments while audio tracks carry sampled sound.

```text
audio/MIDI input → Ardour tracks → plugins → buses → master → audio system → hardware
```
This is a user-level signal model, not an invented account of internals. UI and backend details are version-dependent; consult the official manual for the installed release. Revisit [DAW concepts](../part-04-the-digital-audio-workstation/README.md).

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
