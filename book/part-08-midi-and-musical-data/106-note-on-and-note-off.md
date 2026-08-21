# Chapter 106 — Note On and Note Off

A note lifecycle begins with **Note On** and ends with **Note Off**. Note number selects pitch input; attack velocity is a value the receiver may interpret. A sequencer may store `start + duration`, but transmission turns that convenient record into two timed messages.

```text
NOTE ON → voice begins → time passes → NOTE OFF → voice releases/stops
```

The [Part V voice manager](../part-05-synthesizers/55-polyphony-and-voice-management.md) tracks exactly this state transition. The lab sends note 60 at tick 0 and releases it at tick 480. `Router.route` pairs both messages, creates a `SynthNote`, and renders it. MIDI 1.0 convention also permits Note On with velocity zero to act as Note Off; our router recognizes it.

**Debugging.** Remove the release. The validator accepts each individual message, but lifecycle inspection reports `stuck note: missing note_off`. Evidence is the nonempty active-note table; the fix is a matching release on the same note and channel.

## References

- MIDI Association, [MIDI specifications and resources](https://midi.org/specs), especially MIDI 1.0, Standard MIDI Files, and MIDI 2.0 overview materials; access was attempted 2026-08-21 but blocked by the environment proxy. Protocol claims here are restricted to stable, specification-level semantics recorded in the [Part VIII source note](../../references/source-notes/part-08.md).
- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), for sequencing and computer-music terminology; see [bibliography 29](../../references/bibliography.md#29).
