# Chapter 79 — Delay

## Hear → see → describe

A pure discrete delay is `y[n] = x[n-D]`, with zeros before the input exists. `D` is samples. Convert deliberately: `D = delay_seconds × sample_rate`, or `milliseconds × sample_rate / 1000`. A feed-forward echo is `y[n] = x[n] + g x[n-D]`.

## Implement, break, debug, verify

Compare dry and reverberated examples. Short delays color timbre; longer ones become separate echoes. **Units bug:** treating 250 ms as 250 seconds gives 12,000,000 rather than 12,000 samples at 48 kHz. Write units through the calculation and test the first nonzero index.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
