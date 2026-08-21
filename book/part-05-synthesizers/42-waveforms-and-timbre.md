# Chapter 42 — Waveforms and Timbre

At equal fundamental pitch and amplitude, sine, square, saw, and triangle waves need not sound alike. A sine contains one sinusoidal component. Ideal square and saw shapes require harmonic components; triangle energy falls away differently. The generated shapes are naive educational waveforms and can alias at high pitches—sampling theory belongs to Part VI.

Run the generator and compare four `waveform-*.wav` files while holding playback gain fixed. In `waveforms.svg`, inspect shape before listening. Describe differences in your own terms: brightness, smoothness, edge, density, or another observation are prompts, not prescribed answers.

`harmonic-preview.svg` is only a spectrum-related preview: complex shapes can be described as components at frequencies. Fourier analysis waits until Part VII.

**Debug lab.** Change the square condition from `cycle < .5` to `cycle < 50`. It becomes constant because normalized phase is 0..1. Inspect minimum/maximum and duty cycle before blaming playback.

## References
See Roads [29] and Smith [4].
