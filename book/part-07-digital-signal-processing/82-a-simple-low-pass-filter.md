# Chapter 82 — A Simple Low-Pass Filter

## Hear → see → describe

The educational one-pole rule is `y[n] = y[n-1] + α(x[n] - y[n-1])`. Current input and previous output are normalized samples; `α` is dimensionless in `(0,1]`. The previous output is state. Smaller alpha smooths more. This is not a production filter-design recipe.

## Implement, break, debug, verify

Apply it to the rich source and inspect `filter-eq.svg`. **Break it three ways:** use invalid alpha, omit the state assignment, or reset state for every sample. Rejection, silence/static output, and passthrough-like behavior are distinct evidence. Test attenuation and block equivalence.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
