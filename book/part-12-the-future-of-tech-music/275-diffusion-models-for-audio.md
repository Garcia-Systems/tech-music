# Chapter 275 — Diffusion Models for Audio

## Model

Diffusion training corrupts data across noise levels and learns a denoising objective; sampling begins from noise and iterates a learned reverse process. Audio systems may apply this in waveform, spectrogram, or latent spaces. Diffusion is one family, not a synonym for generative audio.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Vaswani et al. 2017](../../references/bibliography.md#part-xii-sources); [Copet et al. 2023](../../references/bibliography.md#part-xii-sources); [Ho et al. 2020](../../references/bibliography.md#part-xii-sources).
