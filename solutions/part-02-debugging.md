# Solution — Part II Debugging Lessons

1. `60 / bpm` has `(seconds/minute) / (beats/minute) = seconds/beat`; at 120 it is 0.5. The original was mathematically and temporally wrong.
2. Human step 5 maps to index 4, so inspect `snare[4]`. This is a temporal off-by-one error.
3. Divide the semitone distance by 12, not 6: `440 * 2 ** ((note - 69) / 12)`. A5 is 880 Hz. This is mathematical and perceptually obvious.
4. Use `(0,4,7)`, producing `[60,64,67]`. The original ran successfully but was semantically wrong for its `major_triad` name.

Useful assertions are `seconds_per_beat(120) == .5`, `snare[4] == 1`, `isclose(octave_frequency(81), 880)`, and `major_triad(60) == [60,64,67]`. None asserts that a listener must prefer the result.
