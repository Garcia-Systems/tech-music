# Solution — Part V capstone debugging

1. The reference-note change makes note 60 equal 440 Hz. Restore `(note - 69) / 12`; assert notes 69 and 81 are 440 and 880 Hz.
2. The raw mix can exceed ±1. Lower source gains or apply an intentional mix policy before WAV conversion; assert the rendered peak is at most 1.
3. Release must start from the last gated value and reach zero. Inspect the largest adjacent-sample jump; restore continuity and assert the final envelope value.
4. `one_pole_lowpass` accepts hertz. Supply a cutoff such as 1200 Hz and retain validation against zero and Nyquist; name units at the interface.
5. `note_off` must remove the matching active note (a production design may instead retain it in release state). Assert active state after the complete event sequence.

These repairs address software correctness. Whether the repaired patch suits the musical role remains a separate listening decision.
