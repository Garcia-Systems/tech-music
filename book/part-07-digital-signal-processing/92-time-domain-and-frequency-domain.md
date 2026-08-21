# Chapter 92 — Time Domain and Frequency Domain

## Hear → see → describe

The time domain shows amplitude over time. The frequency domain shows complex frequency components: magnitude and phase. They are two views of the same finite observations, useful for different questions.

## Implement, break, debug, verify

Inspect `time-frequency.svg` for a sine, rich waveform, and their spectra. A waveform reveals clipping timing; a spectrum reveals harmonics. Do not ask either view to answer every question.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
