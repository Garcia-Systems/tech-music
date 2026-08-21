# Contributing

Use focused changes and preserve the accessible music–math–software connection. Read the [editorial guide](docs/editorial-guide.md), [research standard](docs/research.md), and applicable template. Run `pytest` and `python scripts/check_markdown_links.py` before proposing a change. Add dependencies only when their educational value exceeds setup cost.

## Generated artifacts

Reproducible generated artifacts are outputs of the executable textbook, not
source material. Generated WAV files, rendered plots, reports, MIDI files, and
similar outputs should normally be written below the ignored `generated/`
directory and recreated from committed source code, structured data, and
documented commands. Examples should use the appropriate `generated/audio/`,
`generated/plots/`, `generated/reports/`, `generated/midi/`, or
`generated/diagnostics/` subtree rather than a book or source-asset directory.

Binary test fixtures or source assets may be committed only when they are
intentionally required and the reason they cannot reasonably be generated in a
temporary directory is documented. This policy applies to all future parts,
including Parts XI and XII.
