# Chapter 85 — Frequency Response

## Hear → see → describe

Magnitude response reports gain versus frequency. Cutoff and attenuation describe a system measurably; resonance can create a peak. Feed known sine tones at constant input amplitude, discard startup, and calculate output RMS/input RMS for each frequency.

## Implement, break, debug, verify

Plot the measured ratios. This is an engineering test: known input → measured output. It validates observable behavior without asserting that the sound is artistically useful.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
