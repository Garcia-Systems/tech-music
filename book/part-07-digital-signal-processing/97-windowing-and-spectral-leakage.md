# Chapter 97 — Windowing and Spectral Leakage

## Hear → see → describe

A finite cut is implicitly multiplied by a window. A rectangular window can spread an off-bin tone across bins. A Hann window tapers endpoints and reduces distant leakage while widening the main lobe; it also changes amplitude scaling.

## Implement, break, debug, verify

The 437 Hz lab does not align with the 62.5 Hz bins. Compare rectangular and Hann traces in `spectral-leakage.svg`. **Debug:** before declaring extra tones, calculate bin spacing and inspect the window.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
