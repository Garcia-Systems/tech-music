# Solution — Part II Capstone Debugging Challenge

The intended constants are `BPM = 120`, `KICK_STEPS = [0,4,8,12]`, `CHORD = [60,64,67]`, `BASS_ENTRY = 8`, and `SECTION_BARS = [2,2,2,2]`. MIDI 63 is outside the declared C-major set; use 62 or 64 according to the intended contour.

These errors cover tempo conversion/design, subdivision placement, scale membership, chord semantics, layer entry, and section duration. Assertions can establish the declared contract, but listening remains useful for finding where a symptom occurs and judging whether a technically valid alternative was actually intended.
