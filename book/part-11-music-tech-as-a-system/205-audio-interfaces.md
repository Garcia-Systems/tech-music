# Chapter 205 — Audio Interfaces

> **Status:** reviewed educational model. Hardware behavior is not probed.

An audio interface bridges analog connections and computer audio. Depending on design it may provide microphone preamps, instrument/line inputs, ADC, DAC, monitor and headphone outputs, direct monitoring, and sometimes MIDI I/O. Exact internal routing varies.

```mermaid
flowchart LR
M[Microphone]-->P[Preamp]-->A[ADC]-->C[Computer / DAW / DSP]-->D[DAC]-->O[Monitor output]-->S[Speaker]
```
Select the intended input, output, channel count, sample rate, and clock configuration; a visible device alone does not establish a complete path.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
