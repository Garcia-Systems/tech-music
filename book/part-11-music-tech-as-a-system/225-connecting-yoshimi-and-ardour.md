# Chapter 225 — Connecting Yoshimi and Ardour

> **Status:** reviewed educational model. Hardware behavior is not probed.

One workflow connects controller events to Yoshimi, then Yoshimi audio to an armed/routed Ardour track, through processing and master to the interface. Alternatives include hosting an instrument plugin in a DAW or sequencing an external synth while recording its audio, when supported.

```text
controller ─MIDI→ Yoshimi ─audio→ Ardour track → DSP/mix → master → interface
```
Verify the MIDI edge and audio edge independently. A monitor path is not necessarily a record path; explicitly choose whether Ardour records MIDI, synthesized audio, or both.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
