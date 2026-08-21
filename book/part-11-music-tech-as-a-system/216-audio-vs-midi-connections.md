# Chapter 216 — Audio vs MIDI Connections

> **Status:** reviewed educational model. Hardware behavior is not probed.

An audio connection carries a representation of sound; a MIDI connection carries musical/control information. An electric piano's audio output → interface → DAW records that instrument's sound. A MIDI keyboard → computer → Yoshimi sends performance instructions; Yoshimi generates the sound.

MIDI activity without audio can be healthy up to the instrument boundary. Audio without MIDI can be expected for a microphone. Name every edge's type—audio, MIDI/event, control, or device communication—to prevent category errors.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
