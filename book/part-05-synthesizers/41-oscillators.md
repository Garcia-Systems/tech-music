# Chapter 41 — Oscillators

An oscillator produces a repeating signal. One **cycle** returns through the waveform's repeating path. Frequency counts cycles per second (hertz), so `period = 1 / frequency`. At sample rate `R`, `samples per cycle = R / frequency`; this need not be an integer. Amplitude scales displacement and phase chooses a starting position within the cycle.

A mathematical curve is continuous; `oscillator` evaluates it only at sample instants. For A4, 440 cycles occur each second. Run `python examples/part_05_synth.py`, inspect `waveforms.svg`, and play `waveform-sine.wav`. Parameters include frequency, amplitude, duration, sample rate, phase (cycles), and waveform.

**Debug lab.** Replace `frequency * n / sample_rate` with `frequency * n * sample_rate`. Predict the symptom, measure zero crossings, then restore the division. A program can run while its units are wrong.

## References
See Roads [29] and Smith [4].
