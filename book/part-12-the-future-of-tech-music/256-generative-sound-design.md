# Chapter 256 — Generative Sound Design

## Model

Generating a patch is safe only when oscillator names, amplitude, envelopes, cutoff, and modulation remain valid for the renderer. Choose from known-safe presets or validate every generated field. An invalid cutoff or excessive gain must fail at the configuration boundary, not become unstable or clipped audio.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Roads 1996](../../references/bibliography.md#part-xii-sources); [Nierhaus 2009](../../references/bibliography.md#part-xii-sources).
