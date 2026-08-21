# Chapter 120 — MIDI vs Audio

| Property | MIDI/event data | Audio |
|---|---|---|
| Represents | instructions/events | signal samples |
| Editable pitch | often easy | more complex |
| Editable timing | often easy | needs audio editing/time processing |
| Produces sound alone | no | playback system required, but audio represents the signal |
| Typical size | small | much larger |
| Depends on instrument | yes | rendered sound already reflects it |
| Change patch later | usually | not in the same way |

The experiment keeps `phrase-events.json` fixed and renders `same-events-sine.wav` and `same-events-saw.wav`. The event data is unchanged; the audio samples differ because the patch differs. `midi-vs-audio.svg` shows the boundary. Audio is still data and requires playback hardware, but unlike MIDI note instructions it already represents the changing signal.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
