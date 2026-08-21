# Chapter 208 — Preamps and Gain Staging

> **Status:** reviewed educational model. Hardware behavior is not probed.

A microphone signal often needs preamplification before ADC. Input gain affects the wanted signal and analog noise reaching conversion; excessive level may clip before any DAW fader. A later fader changes an already converted stream and cannot undo analog clipping.

```text
Microphone → preamp (gain/headroom) → ADC → DAW processing → master → DAC
```
Observe each stage. Establish useful level with margin at the source and preamp, then manage internal and output levels. Gain staging is system-wide, not a ritual of setting every meter to one magic value.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
