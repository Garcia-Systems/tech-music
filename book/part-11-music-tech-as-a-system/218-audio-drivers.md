# Chapter 218 — Audio Drivers

> **Status:** reviewed educational model. Hardware behavior is not probed.

A driver mediates hardware operations and exposes supported streams, formats, timing, controls, and buffers through a platform interface. Applications or audio services negotiate configuration rather than assuming every device supports every sample rate or channel layout.

Correct samples delivered too late are still a real-time failure. Observe configured device, rate, period/buffer, channel map, error/xrun counters, and application logs. Driver architecture and terminology are platform-specific.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
