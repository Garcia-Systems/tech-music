# Chapter 86 — Distortion and Waveshaping

## Hear → see → describe

Distortion is nonlinear: output is not proportional to input. Hard clipping limits values abruptly. Soft clipping uses a smooth rule such as `y = tanh(d x)/tanh(d)`, where `d` is dimensionless drive. Nonlinearity adds harmonics to a sine.

## Implement, break, debug, verify

Compare clean, hard-clipped, and soft-clipped WAVs and `waveshaping.svg` at low volume. **Debug:** if distortion appears before its intended stage, inspect intermediate peaks. Intentional nonlinear processing has an explicit stage and test; accidental clipping does not.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
