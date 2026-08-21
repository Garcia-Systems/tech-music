# Solution — Part VI digital-audio debugging

1. **Rate mismatch:** 48,000 frames tagged 44,100 frames/s lasts 1.0884 s and a
   440 Hz tone plays at 404.25 Hz. Correct metadata or perform real resampling.
2. **Near-silence:** scaling normalized floats by 128 barely occupies PCM16. Use
   the tested mapping `-1 → -32768`, `0 → 0`, and `1 → 32767`.
3. **Channels:** stereo has two values/frame. Deinterleave `L0,R0,L1,R1` and
   verify sentinel arrays before audio. These tests establish consistency, not
   subjective quality.
