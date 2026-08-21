# Chapter 214 — MIDI Keyboards Under the Hood

> **Status:** reviewed educational model. Hardware behavior is not probed.

A key press changes a sensor state. Controller electronics interpret it, form an event (often including note and velocity), transport it over MIDI or USB, and expose it through an operating-system port to an application and instrument.

```text
key → sensor → controller electronics → message → transport → OS → application → instrument
```
This is conceptual: sensing and scanning implementations vary. A lit controller display does not prove that the application receives the intended port or channel.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
