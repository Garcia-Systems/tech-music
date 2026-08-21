# Chapter 29 — MIDI Tracks

Here, “MIDI-style” means editable musical-event data—not the complete MIDI wire protocol taught in Part VIII. A note event has a pitch, start, duration, and velocity; a channel can distinguish destinations, while controller events describe changing performance controls. A piano roll maps time horizontally and pitch vertically. A rhythmic grid emphasizes onset subdivisions; a list exposes exact values.

Part III's `Event` objects are one dataset with multiple representations:

```python
from tech_music.production import loop_events, grid_svg
notes = [e for e in loop_events() if e.pitch is not None]
print([(e.start, e.pitch, e.duration, e.velocity) for e in notes])
grid_svg(loop_events(), __import__('pathlib').Path('assets/part-04/midi-grid.svg'))
```

A piano-roll view would draw each note as a rectangle: `x=start`, `width=duration`, `y=pitch`. The list, grid, and roll do not create three performances; they are projections of one model.

**Quantization** moves times toward a chosen grid. It can correct accidental offsets, but it can also remove intended timing. The event track produces no audio until routed to an instrument. Instrument synthesis remains Part V; protocol details remain Part VIII.

## Ardour connection
The proposed Ardour exercise asks the reader to locate corresponding event-editing concepts in the manual for the installed version; no current UI behavior is asserted here.

## References
See Roads [29] for sequencing; see the source note for the pending Ardour documentation audit.
