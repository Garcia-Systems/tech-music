# Chapter 211 — Sample Clocks

> **Status:** reviewed educational model. Hardware behavior is not probed.

A sample clock supplies the timing reference for conversion. One device producing 48,000 samples per nominal second and another consuming according to an unrelated clock can drift unless the system provides synchronization or rate adaptation. Digital-device configurations therefore identify a clock source as well as a nominal sample rate.

Clicks, periodic artifacts, loss of lock, or failure to start can be consistent with clock/configuration trouble, but are not proof. Check documented clock roles, reported rate/lock, and one boundary at a time. Do not randomly change clock sources while recording.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
