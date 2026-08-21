# Tech Music: Music, Software, and the Computer Science of Sound

> An executable textbook exploring electronic music through music theory, digital audio, synthesis, DSP, software engineering, and computer science—with runnable labs, debugging lessons, exercises, tests, and research-backed references.

## What is “tech music”?

Here **tech music is the book's organizing concept**, not a claim about an established academic genre: primarily digital, often instrumental electronic music that can complement focused technical work and reward creation, study, and engineering. The project asks why music can enrich computer-centered work, without claiming that electronic music is better than live performance, singing, guitar, piano, or any other tradition.

The reader progresses through **Listen → Compose → Produce → Inspect → Experiment → Debug → Program → Build**. The book is for programmers learning music, musicians learning technology, and curious newcomers to both.

## Why executable?

Concepts become small programs, plots, generated audio, measurements, deliberate bugs, and automated tests. A recurring cycle is **Concept → Working Example → Run It → Break It → Observe It → Diagnose It → Fix It → Explain Why**. Listening supplies musical evidence; plots and tests supply measurable evidence. Python favors transparent implementations over unnecessary infrastructure.

## Status

Parts I–III are complete research-informed executable drafts. Part II adds nine music-fundamentals chapters, reusable timing/pitch/event helpers, listening and debugging labs, and a generated musical-sketch capstone. Ardour will be the DAW case study and Yoshimi the synthesizer case study, always after general principles.

## Quick start

Python 3.10+ is required:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m tech_music.waveform
python -m tech_music.music
pytest
python scripts/check_markdown_links.py
```

The example creates `assets/audio/a4-sine.wav` and `assets/waveforms/a4-sine.svg`; generated artifacts are ignored because they are reproducible. Open the SVG, then play the WAV with any local player.

## Repository map

- [`book/`](book/README.md): complete reading order and chapter tree.
- [`src/tech_music/`](src/tech_music/): reusable educational implementations.
- [`examples/`](examples/): runnable and intentionally broken examples.
- [`labs/`](labs/): reproducible lab guides.
- [`exercises/`](exercises/) and [`solutions/`](solutions/): student work separated from reasoned answers.
- [`tests/`](tests/): executable claims and regression checks.
- [`assets/`](assets/): generated visual/audio destinations (not committed binaries).
- [`docs/`](docs/): contributor contracts, roadmap, and research policy.
- [`references/`](references/bibliography.md): inspected sources and source notes.

## Developing the next chapter

Start from the [chapter template](docs/chapter-template.md), choose executable work only where it improves understanding, record inspected sources per the [research standard](docs/research.md), add a reproducible [lab](labs/TEMPLATE.md), and test measurable claims. Keep student-facing debug prompts separate from solutions. See [CONTRIBUTING](CONTRIBUTING.md).
