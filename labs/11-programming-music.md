# Lab 11 — Programming Music

1. Run `tech-music validate data/part-10-project.json`, then inspect it.
2. Run `python examples/part_10_app.py`. Inspect the WAV in
   `generated/audio/part-10/`, four SVG views in `generated/plots/part-10/`,
   and diagnostic report in `generated/reports/part-10/`; reconcile duration,
   peak, event count, and routes.
3. Validate `part-10-broken-project.json`. For each diagnostic, identify the data, timing, instrument, DSP, routing, persistence, automation, or block-state layer before fixing a copy.
4. Add one event in JSON without editing Python. Add one compatible processor in code with focused and pipeline tests.

Success means explaining each boundary from musical idea to PCM—not merely producing a file. See Chapters 162–198 and `tests/test_app.py`.
