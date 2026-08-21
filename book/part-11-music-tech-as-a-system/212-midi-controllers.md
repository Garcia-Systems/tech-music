# Chapter 212 — MIDI Controllers

> **Status:** reviewed educational model. Hardware behavior is not probed.

A keyboard, pad, knob, slider, or pedal turns a gesture into structured event/control data. That data normally describes actions rather than carrying the resulting audio.

```text
human gesture → sensor/controller → MIDI or event data → software → synthesizer → audio
```
At each boundary observe the event, port, channel, message/value, destination mapping, instrument response, and only then the audio path. This extends [Part VIII](../part-08-midi-and-musical-data/README.md).

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
