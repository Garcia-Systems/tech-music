# Chapter 232 — Diagnosing Latency

> **Status:** reviewed educational model. Hardware behavior is not probed.

First define the symptom and path: controller-to-synth, mic software monitoring, or playback? Record configuration and establish a repeatable observation. Compare direct and software monitoring where safely available; bypass high-latency routes/plugins one at a time; inspect buffers, device, rate, system load, and xruns.

Measure and isolate instead of changing random settings. Smaller buffers shorten block duration but reduce the time available to meet each processing deadline. Restore one variable at a time and verify the original musical task.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
