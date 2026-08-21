# Chapter 50 — Additive Synthesis

Additive synthesis builds a complex sound by summing simpler components. In the lab, component `k` is a sine at `k × fundamental`; such integer-related partials are harmonics. Real sounds may also contain inharmonic or changing partials.

Generate fundamental only, add a second harmonic, then use `[1, .5, .33, .25, .2]`. Play `additive.wav` and inspect `harmonic-preview.svg`. Plot components separately before the sum so cause remains visible. The helper scales only if the sum exceeds headroom.

More partials require more oscillator evaluations and additions per sample. That is a computational-cost observation, not a demand to optimize this readable lab prematurely.

## References
See Roads [29] and Smith [4].
