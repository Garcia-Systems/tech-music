# Part VII — Digital Signal Processing

Part VI represented sound as normalized samples. This part asks what algorithms do to them: **hear → see → describe → express mathematically → implement → break → debug → verify**.

## Reading order

1. [Audio as a Signal](76-audio-as-a-signal.md)
2. [Gain](77-gain.md)
3. [Mixing Signals](78-mixing-signals.md)
4. [Delay](79-delay.md)
5. [Feedback Delay](80-feedback-delay.md)
6. [Filters as Systems](81-filters-as-systems.md)
7. [A Simple Low-Pass Filter](82-a-simple-low-pass-filter.md)
8. [High-Pass and Other Basic Filters](83-high-pass-and-other-basic-filters.md)
9. [Equalization](84-equalization.md)
10. [Frequency Response](85-frequency-response.md)
11. [Distortion and Waveshaping](86-distortion-and-waveshaping.md)
12. [Dynamic Range and Compression](87-dynamic-range-and-compression.md)
13. [Envelope Followers](88-envelope-followers.md)
14. [Reverb](89-reverb.md)
15. [Impulse Responses](90-impulse-responses.md)
16. [Convolution](91-convolution.md)
17. [Time Domain and Frequency Domain](92-time-domain-and-frequency-domain.md)
18. [Fourier Series Intuition](93-fourier-series-intuition.md)
19. [The Discrete Fourier Transform](94-the-discrete-fourier-transform.md)
20. [The Fast Fourier Transform](95-the-fast-fourier-transform.md)
21. [Spectral Analysis](96-spectral-analysis.md)
22. [Windowing and Spectral Leakage](97-windowing-and-spectral-leakage.md)
23. [The Short-Time Fourier Transform](98-the-short-time-fourier-transform.md)
24. [Effects Chains](99-effects-chains.md)
25. [Stateful vs Stateless DSP](100-stateful-vs-stateless-dsp.md)
26. [Block Processing](101-block-processing.md)
27. [Numerical Stability and Precision](102-numerical-stability-and-precision.md)
28. [DSP Testing](103-dsp-testing.md)
29. [Debugging DSP](104-debugging-dsp.md)

## Capstone — Mini DSP Rack

`tech_music.dsp.DSPRack` accepts ordered gain, low-pass, distortion, and feedback-delay stages, including bypass flags. It validates configuration, persists processor state, processes deterministic offline blocks, and reports rate, frames, peaks, RMS, clipping, and the realized chain. `examples/part_07_dsp.py` generates its WAV output, diagnostic JSON, and figures. This readable schema is educational, not an interchange standard or production plugin host.

### Broken-chain investigation

Start with gain 3, delay `milliseconds: 250000`, feedback 1, a filter recreated per block, reversed order, and an exported 44.1 kHz tag for 16 kHz samples. For configuration and implementation separately follow **Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix → Verification**. Verify peak, delay samples, feedback validation, whole/block equality, saved order, and WAV rate.

## Listening and visual lab

Run `python examples/part_07_dsp.py`. At low volume compare clean/clipped, dry/reverberated, rich/filtered, hard/soft distortion, compressed/uncompressed, and rack ordering. Generated assets are deterministic and ignored by Git. No copyrighted recordings are used. The SVG set covers transformations, gain/mix/cancellation, delay/reverb, filters/EQ, waveshaping, dynamics/envelope, impulse/convolution, time/frequency, Fourier components, leakage, chains, and blocks.

## End-of-part model

```text
audio samples + parameters + previous state
                    ↓
               DSP algorithm
                    ↓
       new samples + updated state
```

DSP operates on samples. Part VIII will instead ask how notes, controls, timing, and musical events are represented; Part IX asks how processing runs continuously; Part X combines events, synthesis, DSP, and architecture. This part does not begin those subjects.

## References

See every chapter's sources and the [Part VII bibliography](../../references/bibliography.md#part-vii-sources).
