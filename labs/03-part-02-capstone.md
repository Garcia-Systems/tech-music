# Part II Capstone — Build a Musical Sketch

## Design contract
Create a short structural sketch, not a polished production. Declare BPM and meter; rhythm data; scale or pitch collection; bass; chordal material; a short motif; a repeated identity; at least one intentional variation; and named arrangement sections.

The supplied example is 120 BPM, 4/4, C-major pitch material. It combines root-oriented bass, C/F/G-related triads, a motif whose return changes one pitch and octave, and four two-bar sections.

```bash
python -m tech_music.music --bpm 120 --output-dir assets/part-02
```

This generates `musical-sketch.wav` and `arrangement.svg`. The audio uses deliberately plain sine tones so pitch and timing remain inspectable. The SVG shows section width and active layers. There is no drum synthesizer yet: bass and chord/motif attacks serve as timing evidence, while the arrangement diagram includes the designed drum layer. This is an explicit limitation, not a claim of finished production.

## Build your version
1. Copy `capstone_events()` into a new function.
2. State the pitch pattern and chord interval collections.
3. Change one element at a time; keep A and A′ versions.
4. Update the section/layer records.
5. Generate both artifacts, inspect file metadata and timestamps, listen at a safe level, and explain your intentional variation.

## Debugging challenge
Run `python examples/broken_musical_sketch.py` and debug through **listening and inspection**. Do not open the solution first.

Clues: tap the expected tempo; print kick differences; test melody pitch classes; subtract chord notes from the root; compare the bass entry with section boundaries; and sum section bars. Valid Python is not proof of musical intent. The complete repair is in [the solution](../solutions/part-02-capstone.md).
