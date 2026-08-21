# Chapter 202 — Memory and Music Workloads

> **Status:** reviewed educational model. Hardware behavior is not probed.

Storage capacity and working memory answer different questions. A 500 GB library can remain on disk while only selected sample pages, instrument state, waveform caches, buffers, plugin state, and undo history occupy RAM. Streaming trades memory use for storage I/O and scheduling work.

Inventory resident data separately from durable data. If pressure appears, observe process memory and cache behavior before assuming the disk library must fit entirely in RAM. Revisit [memory and streaming](../part-09-computer-science-of-music/146-memory-in-audio-software.md).

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
