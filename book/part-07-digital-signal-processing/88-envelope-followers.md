# Chapter 88 — Envelope Followers

## Hear → see → describe

An envelope follower turns a rapidly alternating waveform into slowly varying control data. It rectifies with `abs`, then smooths with distinct attack and release coefficients. Compressors, meters, modulation, and effects can consume that control signal.

## Implement, break, debug, verify

Plot waveform and envelope in `compression-envelope.svg`. On a level step, verify attack rises faster than release falls. The envelope is not the audio waveform and has no sign.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
