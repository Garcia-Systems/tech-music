# Chapter 119 — MIDI Routing

MIDI routing moves events among sources, ports, tracks, channels, and destinations. Audio routing moves generated signal samples. They may be adjacent in a DAW but are different paths.

```text
Controller → DAW/sequencer → MIDI track/port → synthesizer
                                               ↓
Speakers ← audio bus/track ← audio samples ← instrument
```

`midi-routing.svg` and `channel-routing.svg` expose both stages. **Debugging:** when events exist but no sound follows, ask **Where does the event stop?** Inspect source log, track input, channel/port route, instrument event input, active voices, then audio meters. The router intentionally rejects nonexistent destinations.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
