# Chapter 220 — Linux Audio: JACK

> **Status:** reviewed educational model. Hardware behavior is not probed.

JACK is designed around low-latency, synchronous processing and explicit connections among client ports. Its routing is a graph: clients/ports are nodes and connections carry audio or MIDI data. A process callback must finish its work within the server's cycle.

```text
Yoshimi outputs → JACK routing → Ardour inputs → Ardour master → audio device
```
This is one possible configuration, not a universal setup. Observe registered clients, ports, connections, cycle size, sample rate, and xruns.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
