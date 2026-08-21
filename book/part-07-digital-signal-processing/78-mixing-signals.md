# Chapter 78 — Mixing Signals

## Hear → see → describe

Sample-aligned mixing is `y[n] = x1[n] + x2[n]`. Source levels accumulate, so two safe tracks can make an unsafe bus. Equal signals add; equal polarity-opposed signals cancel. Phase and alignment therefore make mixing more than placing tracks together.

## Implement, break, debug, verify

Hear the three-tone layer and inspect `gain-mixing.svg`; inspect exact cancellation in `phase-cancellation.svg`. Break the mix by summing loud voices. Measure every source and bus, form hypotheses about level and phase, then verify corrected headroom.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
