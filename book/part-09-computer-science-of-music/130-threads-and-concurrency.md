# Chapter 130 — Threads and Concurrency

![Chapter 130](../../images/chapters/130.png)

UI, audio, disk streaming, MIDI input, and analysis have different schedules. Concurrent execution improves responsiveness but creates ordering and ownership problems. A race occurs when results depend on uncontrolled interleaving; reproduce it with a deterministic staged simulation rather than a flaky test.

```mermaid
flowchart LR
UI[UI thread]--messages-->Q[(Queue / snapshots)]-->A[Audio thread]
D[Disk worker]--prefetched blocks-->A
M[MIDI input]--timestamped events-->Q
```

## Try it

Run `python examples/part_09_engine.py`; inspect `src/tech_music/engine.py` and the corresponding tests. Treat all callback timing as simulation.

## Debugging question

Which boundary owns the failing state, what timestamp or ID proves it, and does the evidence show a wrong value or a late value?

## References

- JACK Audio Connection Kit, [Client callbacks / process-thread constraints](https://jackaudio.org/api/group__ClientCallbacks.html); retrieval attempted 2026-08-21 (HTTP 403 in build environment).
- PipeWire project, [Overview and graph model](https://docs.pipewire.org/page_overview.html); retrieval attempted 2026-08-21 (HTTP 403 in build environment).
- ALSA project, [PCM interface documentation](https://www.alsa-project.org/alsa-doc/alsa-lib/pcm.html); retrieval attempted 2026-08-21 (HTTP 403 in build environment).
- LV2, [Architecture overview and specification links](https://lv2plug.in/pages/architecture-overview.html); retrieval attempted 2026-08-21 (HTTP 403 in build environment).
- CLAP, [1.x feature overview and specification](https://cleveraudio.org/1-feature-overview/); retrieval attempted 2026-08-21 (HTTP 403 in build environment).
- Ardour Manual, [Development documentation](https://docs.ardour.org/development/); retrieval attempted 2026-08-21 (HTTP 403 in build environment).
- Yoshimi project, [User guide](https://yoshimi.github.io/docs/user-guide/); retrieval attempted 2026-08-21 (HTTP 403 in build environment).
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2017 (interfaces and boundaries).
