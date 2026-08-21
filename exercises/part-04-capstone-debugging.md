# Part IV debugging capstone — Follow the signal

Work from a copy of `data/part-04-broken-session.json`; do not edit the fixture or open the solution first.

1. Run `python -m tech_music.daw your-copy.json` and preserve diagnostics.
2. Draw or list the timeline and routing graph even when rendering is blocked.
3. Repair five independent fault classes: missing region source, track without an output path, processor parameter outside its contract, automation outside intended time/range, and clipping after excessive summing/gain.
4. For each record **Symptom → Evidence → Hypothesis → Investigation → Root cause → Fix → Verification**.
5. Follow source → region → active track → processor → bus → master → output. Inspect the rendered waveform and run tests after structural validation passes.

Validation passing is not proof the repaired mix sounds good. Add one listening observation separately.
