# Chapter 67 — PCM

**Pulse-Code Modulation (PCM)** is a sequence of quantized sample values representing an audio signal. For one mono excerpt it might be:

```text
0, 1200, 2500, 1800, 0, -1800, -2500, -1200, 0
```

These are not pitches or pressure values by themselves. Interpretation requires sample rate, numeric encoding/bit depth, channel count, and ordering. Real audio has vastly more values: one second of stereo at 48 ksample/s has 48,000 frames and 96,000 channel sample values.

![PCM samples](../../assets/part-06/pcm-samples.svg)

PCM maps naturally to arrays and buffers. A buffer is a finite working block; a file may contain many blocks plus metadata. **Raw PCM** is only encoded sample bytes. A WAV file is a container that can hold PCM and describe it; WAV and PCM are not synonyms.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), [bibliography §29](../../references/bibliography.md#29).
- Julius O. Smith III, *Mathematics of the DFT*, 2nd ed. (2007), [bibliography §4](../../references/bibliography.md#4).
- Additional chapter-specific standards and official documentation are indexed in the [Part VI sources](../../references/bibliography.md#part-vi-sources).
