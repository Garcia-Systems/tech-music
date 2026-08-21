# Part VIII — MIDI and Musical Data

**Audio data describes a changing signal. MIDI describes musical/control events and values.** A MIDI note is not sound. Read Chapters 105–124 in order, then run the lab and capstone. This part completes event/control foundations and does not begin Part IX.

## Chapters

105. [What Is MIDI?](105-what-is-midi.md)
106. [Note On and Note Off](106-note-on-and-note-off.md)
107. [Note Numbers and Velocity](107-note-numbers-and-velocity.md)
108. [MIDI Channels](108-midi-channels.md)
109. [Control Change Messages](109-control-change-messages.md)
110. [Pitch Bend and Expressive Control](110-pitch-bend-and-expressive-control.md)
111. [Aftertouch and Other Performance Data](111-aftertouch-and-other-performance-data.md)
112. [Time, Ticks, and Musical Position](112-time-ticks-and-musical-position.md)
113. [Sequencers](113-sequencers.md)
114. [Piano Rolls](114-piano-rolls.md)
115. [Quantization](115-quantization.md)
116. [Swing and Timing Transformation](116-swing-and-timing-transformation.md)
117. [Tempo Maps](117-tempo-maps.md)
118. [MIDI Files](118-midi-files.md)
119. [MIDI Routing](119-midi-routing.md)
120. [MIDI vs Audio](120-midi-vs-audio.md)
121. [Musical Data Structures](121-musical-data-structures.md)
122. [Event Ordering and Scheduling](122-event-ordering-and-scheduling.md)
123. [Event Validation](123-event-validation.md)
124. [MIDI Debugging](124-midi-debugging.md)

## Execute and verify

```bash
python examples/part_08_midi.py
pytest -q tests/test_midi.py
python scripts/check_markdown_links.py
```

The generator creates nine listening WAVs, thirteen SVG diagrams, original JSON event data, and an SMF format-0 MIDI artifact under `assets/part-08/`. Generated artifacts are reproducible and ignored; the generator and tests are versioned.

## Capstone — Mini MIDI Sequencer

The implementation in `tech_music.midi` supports tempo maps, note-on/off, 0–127 note/velocity values, CC, pitch bend calculations, tracks/channels, validation, offline deterministic scheduling, routing, a piano-roll artifact, synthesis, WAV rendering, and a deliberately narrow SMF round trip.

**Sequence data → validation → timing conversion → scheduler → event router → synthesizer → DSP → audio samples → WAV.** See `sequencer-architecture.svg` after generation. The capstone is educational and offline, not a production DAW or real-time engine.

## Three forms of information

- **Musical structure:** C-major chord.
- **Event data:** `note_on 60`, `note_on 64`, `note_on 67`.
- **Audio signal:** `[0.0, 0.02, 0.06, …]`.

They are related but not interchangeable. Part IX will ask how software processes events and audio continuously under real-time constraints; Part X will combine sequencers, synths, DSP, routing, and interfaces. Those parts are not developed here.
