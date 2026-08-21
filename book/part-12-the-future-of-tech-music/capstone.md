# Part XII Capstone — Adaptive Tech Music

This final major build joins musical rules, probability, events, synthesis, validation, diagnostics, and human controls. It is intentionally a transparent generator—not a commercial AI system and not a productivity intervention.

```text
preferences + seed → validated mode rules → arrangement → note events
                   → Part IX session → synthesizer/render → safe audio
                         ↑ human lock / revise / regenerate
```

## Run and inspect

```bash
python examples/part_12_adaptive.py --mode focus --seed 12 --duration 8
```

The command creates `generated/audio/part-12-adaptive.wav`, `generated/plots/part-12-piano-roll.svg`, and `generated/reports/part-12-generation.json`. These reproducible outputs are ignored. Inspect the report before listening: it contains configuration, arrangement, token stream, and explanations. Change one input at a time; repeat the same seed to verify equality.

Modes (`focus`, `deep-focus`, `light-work`, `break`, `exploration`) are documented musical presets. They do not claim measured effects. Configuration selects a safe patch identifier, constrains tempo, scale, density, variation, duration, and seed, and fails on unknown values. `regenerate` can preserve tempo or events so a person can lock accepted material.

## Evaluation card

| Dimension | Observe | Interpretation |
|---|---|---|
| Technical | valid/order/bounds, finite samples, peak ≤ 1, replay equality | automated invariant |
| Musical | density, repetition, variation, coherence | descriptive plus contextual listening |
| User | enjoyable, distracting, too repetitive/active, fit for stated use | personal report, not binary truth |

A passing technical row cannot establish either other row.

## References

- [Part XII source set](../../references/bibliography.md#part-xii-sources).
- [Executable implementation](../../src/tech_music/generative.py).
