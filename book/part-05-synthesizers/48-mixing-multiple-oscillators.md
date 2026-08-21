# Chapter 48 — Mixing Multiple Oscillators

Synth voices often mix sources. Two identical, phase-aligned oscillators reinforce; an octave layer adds a 2:1 frequency relationship; unlike waveforms combine spectra. Nearby frequencies drift in and out of phase, producing **beating** at their difference rate. Phase affects the instantaneous sum and may affect transients.

Play `detuned-beating.wav` (220 + 222 Hz) and inspect `oscillator-mix.svg`. Then compare same-frequency, octave-apart, detuned, and sine+saw pairs. Balance sources before applying voice-level gain.

Every source consumes headroom. The safe lab averages two oscillators. **Debug lab:** remove `*.5`, inspect the pre-WAV peak, and diagnose clipping through listening, plot, and number rather than one clue alone.

## References
See Roads [29] and Smith [4].
