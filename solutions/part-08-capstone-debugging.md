# Part VIII Capstone Debugging — Solution Outline

1. Validation isolates note 200; replace it with an intended 0–127 note number.
2. The active-note table identifies the missing release; add matching note/channel.
3. The router table exposes the unmapped channel; add a destination or correct it.
4. Label `480 ticks ÷ 480 PPQ = 1 beat = 0.5 s at 120 BPM` before sample conversion.
5. Declare a supported CC-to-parameter mapping; do not invent receiver semantics.
6. Sort simultaneous setup/control, note-off, then note-on under the documented
   policy and retain source order as the final tie-breaker.

Verification is `pytest -q tests/test_midi.py`, an empty active-note table, a
stable schedule across input order, the expected hand-calculated duration, and
inspection of both piano roll and audio render. Passing synthesis tests alone
would not prove that MIDI routing or timing was correct.
