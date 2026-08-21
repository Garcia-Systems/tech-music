# Executable textbook inventory

This inventory separates verified, environment-dependent, and external-system
work. “Verified” means executed in the 2026-08-21 release audit; it does not mean
subjective musical quality was proven.

## Verified in the release environment

- `python -m pytest`: 97 automated tests across waveform, music, production, DAW,
  synthesis, digital audio, DSP, MIDI, engine, app, system, and generation code.
- `python -m tech_music.waveform`: early-book WAV and SVG generation.
- `python examples/part_06_digital_audio.py`: middle-book digital-audio fixtures.
- `python examples/part_12_adaptive.py --mode focus --seed 12 --duration 1`:
  deterministic late-book adaptive audio and event-report generation.
- `python scripts/check_markdown_links.py` and `python scripts/audit_book.py`:
  navigation, numbering, TOC, and tracked-output checks.

The remaining pure-Python examples are covered by the same tested modules but
were not all executed as standalone commands during this audit. Labs 1–13 are
inventoried in `labs/`; their software and listening steps still require a
reader-facing manual pass.

## External or hardware-dependent

Ardour and Yoshimi exercises, audible playback, MIDI controllers, audio
interfaces, ALSA/JACK/PipeWire routing, room monitoring, and real-time latency
measurements were not executed in this headless container. They are optional for
the core Python path and required only by the labs that name them. UI details can
vary by release and Linux audio behavior by distribution and configuration.

## Output policy

New code should write audio to `generated/audio/`, plots to `generated/plots/`,
reports to `generated/reports/`, MIDI to `generated/midi/`, and diagnostics to
`generated/diagnostics/`. Earlier examples retain documented, ignored
`assets/part-*` destinations for compatibility. Never commit a regenerated file
merely to demonstrate that a command ran.
