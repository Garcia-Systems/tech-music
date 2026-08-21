# DAW Concepts Lab — Reconstruct a simplified session

## Objective
Load one readable session, inspect timeline and routing, render its master output, visualize state derived from the same data, and distinguish validation from listening.

## Reproducible procedure

1. Run `python -m tech_music.daw`. The command loads `data/part-04-session.json`.
2. Inspect tempo, two tracks, regions, MIDI-style/generated-audio sources, shared delay bus, routes, automation, markers, and master/output.
3. Open `assets/part-04/timeline.svg`, `routing.svg`, and `waveform-automation.svg`.
4. Play `session-render.wav` at a safe fixed level. Set the shared-delay mix to `0`, render to a separate directory, and compare at matched level.
5. Run `pytest tests/test_daw.py -q`. Explain what each check proves and cannot prove.
6. Change one region start, track gain, mute, or automation point. Predict data, diagram, measurement, and audible effects before rerunning.

## Expected objective result
At 120 BPM, eight beats render as four seconds at 22,050 Hz, mono, without samples at or beyond full scale. Both tracks have a graph path to output. Musical effectiveness remains a listening judgment.

## Reflection
How do arrangement→timeline, layers→tracks, events→MIDI regions, generated sound→audio regions, effects→processors, and variation→automation map back to Part III?

## Limitations
The renderer uses sine sources, one mono sum, a tiny delay, and offline processing. It is not a DAW, reverb, MIDI implementation, plugin host, or real-time engine.
