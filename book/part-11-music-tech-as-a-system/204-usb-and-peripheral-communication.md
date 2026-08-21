# Chapter 204 — USB and Peripheral Communication

> **Status:** reviewed educational model. Hardware behavior is not probed.

USB has a host that schedules communication with connected devices. Device classes can support interoperable audio or MIDI behavior, while product-specific functions may need additional software. Nominal link bandwidth is not end-to-end latency: transfers, buffering, drivers, scheduling, conversion, and applications contribute separately.

A controller can transport MIDI events over USB; an interface can transport sampled audio; a control surface can transport commands. Identify the payload and endpoint rather than saying only “USB is connected.”

## Checkpoint

Draw the relevant path, label every edge by type, and name one observable at each boundary. Connect the result to Parts IV–X rather than treating this layer in isolation.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed., MIT Press, 2023 (computer-music systems and terminology).
- Francis Rumsey and Tim McCormick, *Sound and Recording*, 7th ed., Focal Press, 2014 (recording, conversion, monitoring, and acoustics).
- [Project bibliography and Part XI access/version note](../../references/bibliography.md#part-xi-sources), accessed or retrieval attempted 2026-08-21.
