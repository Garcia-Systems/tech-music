# Chapter 104 — Debugging DSP

## Hear → see → describe

Use the same loop for every fault: **Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix → Verification**. Keep intermediate buffers and units observable.

## Implement, break, debug, verify

1. **Clipping:** peak growth → meter each stage → reduce/shape gain → assert bounds. 2. **Silence:** zeros → trace routing/gain → restore path → nonzero RMS. 3. **Wrong delay:** wrong onset → label ms/samples → divide by 1000 → index test. 4. **Filter failure:** no smoothing → inspect state → persist it → block equivalence. 5. **Unstable feedback:** growing repeats → inspect `f` → require `|f|<1` → bounded impulse. 6. **Wrong spectrum:** wrong label → inspect N/rate/window → map bins → known sine. 7. **Boundary click:** periodic discontinuity → inspect block edges → preserve state → whole/block equality.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
