# Solution: incorrect waveform time base

## Root Cause
`np.arange(...)` produces dimensionless sample indices, but the broken code names them seconds and sends `2π × 440 × n` to sine. At integer `n`, this is mathematically an integer number of full cycles, so ideal values are zero; floating-point roundoff leaves tiny noise.

## Fix
Divide indices by sample rate: `time_seconds = np.arange(sample_count) / sample_rate`. Then calculate `0.5 * np.sin(2 * np.pi * frequency * time_seconds)`.

## Verification
Confirm 44,100 samples, peaks within ±0.5, multiple positive-going crossings, an estimate near 440 Hz, roughly 4.4 cycles in the first 10 ms, and an audible steady tone.

## Engineering Lesson
Names do not establish units. Dimensional reasoning catches defects that valid syntax and plausible array shapes cannot; tests should assert signal meaning as well as data type and length.
