# Chapter 11 — Chords and Harmony

An **interval** is a distance between pitches. A **chord** combines pitches; a **triad** contains a root, third, and fifth when arranged in thirds. In semitone data, `major_triad = [0,4,7]` and `minor_triad = [0,3,7]`. The root supplies identity, while the third distinguishes these two types and the fifth is seven semitones above the root.

```text
C4 piano-roll pitches: 67  ─ G (fifth)
                       64  ─ E (major third)
                       60  ─ C (root)
```

**Harmony** includes simultaneous pitches and how they move. A **chord progression** is an ordered harmonic path. `transpose(root, MAJOR_TRIAD)` generates a chord at any valid root; the capstone makes C, F, G, C material. Pitch-class descriptions ignore octave placement, whereas a piano roll retains register.

**Consonance** and **dissonance** are context-sensitive perceptions and conventions, not fixed emotion buttons. Compare a single note, root+fifth, `[0,4,7]`, `[0,3,7]`, and `[0,1,7]`. Describe beating, roughness, stability, and expectation before assigning labels.

## Debugging semantic correctness
A function can execute successfully while using `[0,5,7]` for a major triad. The list is valid Python and produces valid audio, but its “third” is wrong for the intended abstraction. Listen, inspect intervals, assert `[60,64,67]`, then repair it. Audible and semantic correctness complement runtime success.

## References
See the [bibliography](../../references/bibliography.md): Laitz [24] for intervals, triads, and harmonic function; Sethares [26] for consonance/dissonance and timbre; Huron [27] for expectation in musical listening.
