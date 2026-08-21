# Lab 12 — Trace and Validate a Music-Tech System

This lab models configuration; it does **not** discover or test hardware.

1. Calculate a 10-minute, eight-channel 48 kHz/24-bit PCM payload with `python -m tech_music.system storage --seconds 600 --rate 48000 --bits 24 --channels 8`. State why a real project occupies more space.
2. In Python, compare `buffer_ms(64, 48000)` and `buffer_ms(1024, 48000)`, then compare each deadline with an explicit processing estimate using `deadline_margin_ms`.
3. Validate `data/part-11-workstation.json`. Draw its typed event/audio edges.
4. Validate the broken configuration. For every deterministic finding, identify an observation a real system would require before treating it as a root cause.
5. Copy the broken JSON under `generated/diagnostics/`, repair one fault at a time, and rerun. Generated copies remain ignored.
6. Trace capstone Paths A–C. At every boundary write: expected object, observable, and safe corrective action.

A completed lab explains why MIDI activity is not proof of audio, a monitor path is not proof of a record path, configured buffer duration is not measured round-trip latency, and model validation is not hardware verification.

## References

- [Part XI chapters and capstone](../book/part-11-music-tech-as-a-system/README.md).
- [Project bibliography](../references/bibliography.md#part-xi-sources).
