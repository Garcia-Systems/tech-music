# Debugging the Adaptive Capstone

For every fault, record **Symptom → Evidence → Hypotheses → Investigation → Root cause → Fix → Verification**. Never repair by silent fallback.

1. Give `weighted_choice` zero/negative weights (invalid distribution).
2. Replace the local seeded RNG with module-global randomness (seed ignored).
3. schedule a note past duration (timing).
4. inject MIDI 61 into C minor (constraint).
5. sum voices without bounded gain (clipping).
6. change mode but reuse cached parameters (state).
7. omit seed or schema from saved configuration (persistence).
8. request an unknown mode and silently use focus (validation).
9. Duplicate synthetic sources across train/test (evaluation leakage).

For each fix, add an invariant or deterministic regression test. Listening alone is insufficient; tests alone cannot judge artistic quality.

## References

- [Chapters 291–293](../book/part-12-the-future-of-tech-music/291-debugging-generative-music-systems.md).
- [Tests](../tests/test_generative.py).
