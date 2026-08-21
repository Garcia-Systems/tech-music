# Chapter 46 — Filters

A filter changes frequency content. A low-pass favors content below cutoff, a high-pass favors content above it, and a band-pass favors a region. **Cutoff** names a transition location, not a brick wall. Resonance or Q describes emphasis/selectivity near that region; the one-pole lab deliberately has no resonance control.

Run the lab. `filter-before-after.wav` places the original saw first and the 700 Hz low-pass result second; `filter-comparison.svg` shows their short waveforms. This demonstrates behavior, not a full DSP derivation or perceptual guarantee.

**Debug lab.** Pass 44,100 as cutoff at a 22,050 Hz sample rate. Validation rejects it because cutoff must lie below Nyquist. If code instead normalized cutoff twice, the result could be nearly silent. Inspect units, range, output peak, and before/after content.

## References
See Roads [29] and Smith [4].
