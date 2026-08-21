# Generating a Waveform with Code

A concert A can begin as a number. This chapter follows one tone through **musical pitch → frequency → mathematics → samples → array → waveform → audio**. The same path underlies more elaborate instruments.

## Learning objectives

After completing the chapter, you can:

- relate pitch, frequency in hertz, and cycles;
- explain amplitude without confusing it with frequency;
- evaluate a sampled sine equation;
- generate, inspect, plot, and save a mono tone;
- test sample count, range, and approximate frequency; and
- diagnose a unit error that turns a tone into silence or the wrong signal.

## Musical context

We use A4, conventionally 440 Hz [5], as a convenient reference—not as a rule that every performance or tuning system must follow. **Frequency** counts cycles per second: an ideal 440 Hz periodic wave completes 440 cycles in one second. Frequency strongly relates to perceived pitch, although real pitch perception and musical sounds are richer than this single-tone model.

**Amplitude** describes the signed displacement of our normalized signal. Here `0.5` limits ideal peaks to ±0.5. It controls signal level, not the number of cycles. Perceived loudness is not a simple linear synonym for sample amplitude.

## Conceptual model

```text
A4 pitch → 440 cycles/second → sine equation → 44,100 samples/second
         → Python list → plotted shape + PCM WAV → eyes + ears + tests
```

An array is an ordered sequence of numerical sample values. It is a useful bridge between mathematics and software: each position denotes a time, while its stored value denotes instantaneous amplitude.

## Mathematics, one sample at a time

For sample index `n`, we calculate:

\[
x[n] = A\sin\left(2\pi f\frac{n}{F_s}\right)
\]

- `x[n]` is the sample value.
- `A` is peak amplitude (`0.5`).
- `f` is frequency (`440` cycles/second).
- `n` is the integer sample index (`0, 1, 2, …`).
- `F_s` is sample rate (`44,100` samples/second).
- `n/F_s` converts an index into seconds.
- `2π` converts cycles into radians, the unit expected by Python’s `math.sin` [4].

The first sample is zero because `sin(0) = 0`. About every `44,100 / 440 ≈ 100.23` samples, the phase completes another cycle. A digital array cannot place a sample at a fractional index; the values still describe a correctly sampled 440 Hz sinusoid.

## Executable example

From an installed project environment, run:

```bash
python -m tech_music.waveform
```

The implementation builds explicit sample indices, applies the equation element by element with Python’s standard library, writes 16-bit mono PCM with the `wave` module [1], and draws the first 10 ms as SVG. It does not hide tone generation behind an audio-synthesis library.

Core implementation:

```python
sample_count = round(duration * sample_rate)
samples = [
    amplitude * math.sin(2 * math.pi * frequency * n / sample_rate)
    for n in range(sample_count)
]
```

See [`src/tech_music/waveform.py`](../../src/tech_music/waveform.py) for parameter validation, WAV conversion, plotting, and the CLI.

## Inspect the data

Default output begins approximately:

```text
Generated 44100 samples; first 8: [0.       0.031324 0.062525 0.093481 0.124069 0.15417  0.183665 0.212438]
Estimated frequency: approximately 440 Hz
```

Small numerical differences in formatting may occur across library versions. Check length, minimum/maximum, and zero crossings instead of trusting the filename. The included estimator measures spacing between positive-going zero crossings; it is useful for this clean lesson signal, not a general-purpose pitch detector.

## Visual inspection

Open `assets/waveforms/a4-sine.svg`. In 10 ms you should see a little more than four smooth cycles because `440 × 0.010 = 4.4`. The curve should stay between −0.5 and +0.5 and be centered on zero. A plot can reveal clipping, offsets, discontinuities, and unexpected cycle counts before listening.

## Listening experiment

Play `assets/audio/a4-sine.wav` at a safe monitoring level. Expect a steady, plain tone lasting one second—not an acoustic-piano A. Lower the player volume before experimenting with amplitude. Compare `--frequency 220` and `--frequency 880`; each halving or doubling spans an octave in this reference example.

```bash
python -m tech_music.waveform --frequency 220 --output-dir /tmp/tech-music-220
```

## Debugging lesson: the silent 440 Hz tone

Open [`examples/incorrect_waveform.py`](../../examples/incorrect_waveform.py), but do not open the solution yet.

### Symptom

The array is nearly silent even though it requests 440 Hz and amplitude 0.5. A plot does not show the expected sine curve.

### Evidence

Print the first eight values, maximum absolute value, and positive-going zero-crossing count. Compare the variable name `time_seconds` with its contents.

### Hypotheses

Could amplitude be zero? Is frequency outside the representable band? Is the sine function receiving the wrong angular unit? Was sample index converted to seconds?

### Investigation

1. Evaluate the expression for indices 0 and 1 by hand.
2. State the units of every factor inside `sin`.
3. Compare it with `n / sample_rate` in the working implementation.
4. Make one minimal correction, then rerun the measurements and listen.

Only afterward read the [reasoned solution](../../solutions/incorrect-waveform.md).

## Automated verification

Run `pytest`. Tests verify exactly 44,100 samples, bounded amplitude, a zero-crossing frequency estimate near 440 Hz, deterministic generation, rejected invalid parameters, and WAV channel/sample-width/rate/frame metadata. These tests complement listening; they do not prove subjective musical quality.

## Exercises

1. **Numerical:** calculate the nominal samples per cycle for 220, 440, and 880 Hz at 44,100 samples/second.
2. **Code:** add a `phase_radians` parameter while preserving existing defaults and tests.
3. **Listening:** generate 220, 440, and 880 Hz at equal amplitude. Record what changes and what does not.
4. **Visualization:** plot 5 ms versus 50 ms. Explain the detail/context trade-off.
5. **Debugging:** deliberately omit `2π`; measure the resulting frequency and explain the unit mismatch.
6. **Engineering:** test whether WAV samples remain in the signed 16-bit range at amplitude 1.0.

## Practical challenge

Generate a two-second, 0.25-amplitude C5 tone using an appropriately researched frequency. Add a test that estimates its frequency, create the two artifacts in a temporary output directory, and write down auditory and visual observations. Cite the source of the chosen reference frequency.

## Expected observations and common mistakes

- One second at 44,100 Hz contains 44,100 samples, indexed `0` through `44,099`.
- A4 produces about 4.4 cycles in 10 ms.
- Normalized amplitude 0.5 should not clip during conversion.
- A WAV is generated rather than committed; rerunning is the provenance.
- Common errors include using sample indices as seconds, omitting `2π`, mixing milliseconds and seconds, generating an off-by-one endpoint, and scaling floating samples to integers without clipping.

## Connection to the larger system

A synthesizer oscillator repeatedly performs this kind of phase-to-sample computation. A DAW stores or streams the samples in buffers; routing graphs move them; DSP transforms them; an audio interface converts them for playback. Later chapters will replace this whole-array, offline example with stateful oscillators and real-time buffers.

## Chapter summary

Pitch can be represented by a frequency; time can be represented by sample indices; a periodic equation maps those indices to an amplitude array; and software can plot, encode, hear, and test that array. The sample-rate division is not bookkeeping—it supplies the seconds required for correct pitch.

## References

Numbers refer to the [project bibliography](../../references/bibliography.md).

1. Python Software Foundation, “`wave` — Read and write WAV files.”
2. NumPy Developers, “`numpy.sin`” (comparison and future vectorized work).
3. NumPy Developers, “`numpy.arange`” (comparison and future vectorized work).
4. Julius O. Smith, *Mathematics of the Discrete Fourier Transform (DFT), with Audio Applications*, 2nd ed., especially the sinusoid and sampling material.
5. ISO 16:1975, *Acoustics — Standard tuning frequency (Standard musical pitch)*.
