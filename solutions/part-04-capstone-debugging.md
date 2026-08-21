# Part IV debugging capstone — Reasoned solution

1. **Missing source:** `bass-a.source` names `missing_audio`; point it to the declared `bass_events` or declare a real generated source.
2. **Broken routing:** `orphan` has no outgoing edge. Add `['orphan','master']` while retaining `['master','output']`, then verify `route_path`.
3. **Invalid processor:** `bad-wet.mix=1.4`; choose a documented value in `[0,1]`, such as `0.18`.
4. **Automation:** beat 12 lies beyond the eight-beat session and value 1.2 exceeds the normalized range. Move it to beat 8 and use at most 1.
5. **Clipping:** structural fixes may allow two high-amplitude layers to sum beyond one. Lower track/source gain while preserving balance; inspect peak rather than silently normalizing.

Regenerate timeline, routing, waveform, and WAV; run `pytest tests/test_daw.py -q`. Then listen. A valid graph and safe peak establish objective properties only.
