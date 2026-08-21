# Chapter 76 — Audio as a Signal

## Hear → see → describe

A signal is the ordered sequence `x[0], x[1], …, x[N-1]`; `n` is a dimensionless sample index. Hear the generated tone, inspect its plot, then read `y[n] = process(x[n])`. For `y[n] = 0.5 x[n]`, input and output have the same duration but different amplitude. A **system** maps input to output. Parameters, other signals, earlier samples, channels, and internal **state** may also influence that map.

## Implement, break, debug, verify

Run the generator and compare `clean.wav` with the gain trace in `gain-mixing.svg`. Predict peak first; verify it with `peak`. This continues Part VI's normalized floating-point sample model.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
