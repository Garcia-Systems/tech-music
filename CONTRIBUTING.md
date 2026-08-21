# Contributing

Use focused changes and preserve the accessible music–math–software connection. Read the [editorial guide](docs/editorial-guide.md), [terminology guide](docs/terminology.md), [research standard](docs/research.md), and applicable template. Run `pytest`, `python scripts/check_markdown_links.py`, and `python scripts/audit_book.py` before proposing a change. Add dependencies only when their educational value exceeds setup cost.

Number chapters once, globally and sequentially; use `NN-title.md` and
`# Chapter NN — Title`. Add the chapter to its part index and the master TOC.
Prefer linked titles over bare chapter-number references. A lab states its
objective, prerequisites, command, expected evidence, debugging task,
verification, extension, and cleanup where relevant. Substantive debugging
lessons use **Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix
→ Verification → Engineering Lesson**, with answers kept in `solutions/`.

References must have been inspected. Prefer standards, official documentation,
primary research, and established texts; record access boundaries in source
notes. Test measurable behavior and invariants, not subjective musical quality.

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
