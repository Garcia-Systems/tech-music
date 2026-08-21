# Tech Music: Music, Software, and the Computer Science of Sound

> An executable textbook exploring electronic music through music theory, digital audio, synthesis, DSP, software engineering, and computer science—with runnable labs, debugging lessons, exercises, tests, and research-backed references.

## What is “tech music”?

Here **tech music is the book's organizing concept**, not a claim about an established academic genre: primarily digital, often instrumental electronic music that can complement focused technical work and reward creation, study, and engineering. The project asks why music can enrich computer-centered work, without claiming that electronic music is better than live performance, singing, guitar, piano, or any other tradition.

The reader progresses through **Listen → Compose → Produce → Inspect → Experiment → Debug → Program → Build**. The book is for programmers learning music, musicians learning technology, and curious newcomers to both.

## Why executable?

Concepts become small programs, plots, generated audio, measurements, deliberate bugs, and automated tests. A recurring cycle is **Concept → Working Example → Run It → Break It → Observe It → Diagnose It → Fix It → Explain Why**. Listening supplies musical evidence; plots and tests supply measurable evidence. Python favors transparent implementations over unnecessary infrastructure.

## Status

**Version 0.1.0 release candidate.** Parts I–XII contain a continuous sequence of
307 research-informed draft chapters. The automated suite, structural audit, and
local-link check pass; software- and hardware-dependent labs remain explicitly
unverified. See the truthful [release-readiness checklist](docs/release-readiness.md)
and [release notes](docs/release-notes-0.1.0.md) before publishing.

## Quick start

Python 3.10+ is required:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python -m tech_music.waveform
python -m tech_music.music
python examples/part_05_synth.py
python examples/part_06_digital_audio.py
python examples/part_07_dsp.py
python examples/part_12_adaptive.py --mode focus --seed 12 --duration 8
python -m tech_music.digital_audio assets/part-06/tone-stereo.wav
pytest
python scripts/check_markdown_links.py
python scripts/audit_book.py
```

The first waveform example uses legacy ignored paths under `assets/`; newer
examples write beneath `generated/`. These outputs are reproducible and ignored.
Open the SVG, then play the WAV with any local player.

## Repository map

- [`book/`](book/README.md): master TOC with every chapter, appendix, and capstone.
- [`src/tech_music/`](src/tech_music/): reusable educational implementations.
- [`examples/`](examples/): runnable and intentionally broken examples.
- [`labs/`](labs/): reproducible lab guides.
- [`exercises/`](exercises/) and [`solutions/`](solutions/): student work separated from reasoned answers.
- [`tests/`](tests/): executable claims and regression checks.
- `generated/`: ignored audio, plots, reports, MIDI, datasets, and diagnostics produced by examples.
- [`assets/`](assets/): legacy part-specific generated destinations and versioned teaching diagrams.
- [`docs/`](docs/learning-path.md): learning and reader paths, contributor contracts, glossary, audit records, and release policy.
- [`references/`](references/bibliography.md): inspected sources and source notes.

## Developing the next chapter

Start from the [chapter template](docs/chapter-template.md), choose executable work only where it improves understanding, record inspected sources per the [research standard](docs/research.md), add a reproducible [lab](labs/TEMPLATE.md), and test measurable claims. Keep student-facing debug prompts separate from solutions. See [CONTRIBUTING](CONTRIBUTING.md).
