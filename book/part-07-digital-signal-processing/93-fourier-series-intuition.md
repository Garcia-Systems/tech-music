# Chapter 93 — Fourier Series Intuition

## Hear → see → describe

A periodic waveform can be approximated by adding sinusoids. Hear a fundamental, then add integer-multiple harmonics. Each addition changes shape and timbre; Part V called this additive synthesis.

## Implement, break, debug, verify

Build fundamental → plus third → several odd harmonics and inspect `fourier-series.svg`. More terms improve a square-like approximation but finite sums retain edge ripple.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
