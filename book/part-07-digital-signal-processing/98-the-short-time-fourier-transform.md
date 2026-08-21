# Chapter 98 — The Short-Time Fourier Transform

## Hear → see → describe

Music changes, so one whole-file DFT hides when components occur. The STFT divides audio into overlapping windows, applies a window and FFT to each, and arranges spectra over time as a spectrogram.

## Implement, break, debug, verify

Generate a chirp, use fixed window and hop sizes, and plot time frames against frequency bins. Short windows improve time localization; long windows improve bin spacing. Overlap increases sampling in time but does not erase this tradeoff.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
