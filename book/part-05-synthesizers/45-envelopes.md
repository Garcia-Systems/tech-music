# Chapter 45 — Envelopes

A note changes over time. An ADSR envelope rises during **attack**, falls during **decay**, holds a **sustain level** while the gate remains on, and moves toward zero during **release** after note-off. ADSR is common, not universal.

`adsr_envelope` returns a control curve; multiplication turns a steady oscillator into an articulated note. Run the example to create `adsr.svg` and `envelope-shaped.wav`. Compare fast/slow attack, short decay/low sustain (percussive), and long attack/release (pad-like). Keep pitch and playback level fixed, write observations, and do not treat a preference as a defect.

**Debug lab.** Make release begin at 1 rather than the last gated value. A sample jump can click. Locate it with adjacent-sample differences, then restore continuity. Tests assert length, range, plateau, start, and endpoint.

## References
See Roads [29] and Smith [4].
