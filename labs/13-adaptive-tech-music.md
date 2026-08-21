# Lab 13 — Adaptive Tech Music

1. Run `python examples/part_12_adaptive.py --mode focus --seed 12 --duration 8` twice. Compare report hashes and event tokens.
2. Change only the seed, then only density, then only mode. Explain each observable difference using the decision trace.
3. Call `markov_sequence` with the C/G/F example from Chapter 249. Remove a reachable transition row and interpret the error.
4. Compare uniform and weighted choices over 1,000 trials from a fixed seed; report counts without claiming exact theoretical equality.
5. Encode and decode events. Corrupt one token prefix and confirm validation fails.
6. Use `regenerate(..., lock_events=True)` and verify the locked invariant.
7. Inspect peak, event order, duration, and pitch-set membership. Then complete the musical/user evaluation card separately.

Outputs belong under ignored `generated/`; do not commit them.

## References

- [Part XII](../book/part-12-the-future-of-tech-music/README.md).
