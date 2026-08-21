# Chapter 215 — Drum Pads, Knobs, and Control Surfaces

> **Status:** reviewed educational model. Hardware behavior is not probed.

Physical forms can share an event abstraction: a pad may emit note and velocity; a knob a controller value; a fader a parameter value; a transport button a command. Software maps source identifiers and value ranges onto musical state.

Debug raw input first, then mapping, takeover/scaling behavior, target parameter, and feedback. Do not confuse control feedback to a motorized/display surface with the audio being controlled.

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
