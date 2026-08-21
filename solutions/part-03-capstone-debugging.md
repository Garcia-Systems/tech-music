# Part III capstone debugging solutions

1. **Timing:** grid/data reveal off-grid `2.6`; restore intended `2.5`, regenerate, inspect and listen.
2. **Pitch:** MIDI 24 is one octave below 36; restore 36, compare frequency/register and listen.
3. **Harmony:** `(0,4,7)` is a major rather than intended minor triad; restore `(0,3,7)` and verify event pitches.
4. **Arrangement:** intro layers contain bass; remove it and verify the intro cell and filtered score.
5. **Level:** a peak above 1 clips during PCM conversion; restore normalization to a 0.92 ceiling and assert the sample peak is below 1.

In each report, distinguish the observed symptom from the hypothesis. Run the full suite after the focused check.
