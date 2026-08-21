# Chapter 95 — The Fast Fourier Transform

## Hear → see → describe

An FFT is an efficient family of algorithms for computing the DFT—not a different transform. Direct evaluation takes roughly O(N²) work; common FFT algorithms take roughly O(N log N), with implementation- and size-dependent constants.

## Implement, break, debug, verify

Time small sizes such as 32–256, repeat enough to reduce noise, and avoid treating a microbenchmark as universal. Compare outputs before comparing speed.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
