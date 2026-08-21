# Chapter 105 — What Is MIDI?

MIDI—**Musical Instrument Digital Interface**—is a family of specifications for exchanging musical performance and control information among hardware and software. A message can describe an action such as “play note 60 with velocity 90”; it is not a recording of what that action sounds like. The receiving device, software instrument, mapping, and patch determine the result.

```text
Microphone → audio samples → recorded waveform
Keyboard/controller → MIDI note events → synthesizer → audio samples
```

MIDI 1.0 channel messages, Standard MIDI Files (SMF), General MIDI mappings, and MIDI 2.0 are related but distinct. This part uses a manageable MIDI 1.0/SMF subset: messages, 16 logical channels, notes, controllers, pitch bend, and sequencing. General MIDI is one interoperability profile, not the definition of all MIDI use.

The durable mental model is **musical intent → event → MIDI message → channel/destination → instrument or processor → sound generation → audio**. Compare `note_on 60 velocity 90` with audio `[0.0, 0.03, 0.07, …]`: instruction versus sampled signal.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
