# Chapter 81 — Filters as Systems

## Hear → see → describe

A filter changes frequency relationships. Low-pass retains more low-frequency energy; high-pass retains more high; band-pass selects a region; a notch rejects one. Cutoff is in hertz, while resonance/Q describes emphasis or selectivity. A time-domain recurrence operates on samples; a frequency response describes the same system's behavior by frequency.

## Implement, break, debug, verify

Return to Part V's synthesizer filter and Part IV's plugins. Here the implementation and persistent state become explicit. Listen to one harmonically rich source through each filter before naming the change.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
