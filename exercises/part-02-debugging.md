# Part II Debugging Lessons

Run `python examples/incorrect_music.py`. The program has no syntax or runtime error, yet four results contradict their musical intent.

1. **Tempo:** measure the printed 120 BPM interval. Which ratio has seconds/beat units?
2. **Rhythm:** the human-readable fifth step should contain the snare. Which Python index denotes it?
3. **Pitch:** A5 should be one octave above 440 Hz. Trace every term in the exponent.
4. **Harmony:** compare the generated chord with major-triad offsets `[0,4,7]`.

Classify each symptom as syntactic, mathematical, temporal, musically unintended, or technically valid but perceptually undesirable. Make one repair at a time and add a small assertion. Only then consult the [solution](../solutions/part-02-debugging.md).
