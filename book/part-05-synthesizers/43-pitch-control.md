# Chapter 43 — Pitch Control

A note event becomes oscillator frequency. In twelve-tone equal temperament, `f = 440 × 2^((n - 69) / 12)`: note 69 is A4, twelve semitones double frequency, and pitch bend changes frequency continuously rather than selecting another integer note. Tuning systems can use other mappings; this book's helper explicitly uses this one.

The capstone path is **note → `midi_to_frequency` → `oscillator` → samples**. Generate the example; its final three simultaneous events form a C-major chord. Modify the note numbers to create a scale and compare adjacent steps and octave pairs.

**Debug lab.** In a copy of the formula, use integer division or divide by 10. Check notes 69 and 81 first: reference and octave invariants localize the fault. Audible pitch is evidence; numerical frequency explains it.

## References
See ISO 16 [5], Sethares [26], and Roads [29].
