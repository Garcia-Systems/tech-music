# Chapter 51 — Frequency Modulation Synthesis

In frequency modulation, a **modulator** changes a **carrier's** instantaneous frequency. Modulator frequency determines how fast; depth (here in hertz) determines excursion. The ratio and amount strongly affect the resulting spectrum. Other FM formulations use a dimensionless modulation index, so always read the interface.

Run `fm.wav`, then compare depths 5, 40, and 200 Hz while holding carrier/modulator fixed. Describe, do not rank, the results.

The implementation accumulates phase using `instantaneous_hz / sample_rate`. **Debug lab:** add hertz directly to phase, confusing frequency with cycles per sample. The sound and frequency estimate fail even though each variable is numeric. Write units next to the calculation.

## References
See Roads [29] and Smith [4].
