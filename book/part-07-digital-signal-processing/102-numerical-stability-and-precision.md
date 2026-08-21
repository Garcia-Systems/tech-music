# Chapter 102 — Numerical Stability and Precision

## Hear → see → describe

Floating point rounds; long sums accumulate error; integer PCM can overflow without widening/clipping; tiny denormal values can be costly on some systems; recursive systems can amplify errors. These are engineering constraints, not reasons to distrust all DSP.

## Implement, break, debug, verify

Run `state = 1.001 * state + input` and log peak every 1000 samples. Growth with zero input reveals an unstable recurrence. Bound parameters, choose stable structures, use suitable precision, and test finite values over time.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
