# Part V capstone debugging — Five wrong sounds

Copy the working patch and implementation; do not damage the baseline. Introduce and diagnose each fault separately.

1. **Wrong pitch:** use `(note - 60) / 12` in note conversion.
2. **Clipping:** sum two amplitude-0.8 oscillators without level management.
3. **Click:** begin release at 1 rather than the envelope's current level.
4. **Filter error:** supply normalized `0.2` where the interface requires hertz.
5. **Stuck voice:** make `note_off` leave the note in `active`.

For every fault provide: audible symptom (if playback is available), relevant plot, sample/peak measurement, inspected parameter and unit, failing focused test, signal-flow location, repair, and passing regression test. Do not infer a cause from taste alone.
