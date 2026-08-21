# Chapter 35 — Mixing

Mixing combines signals while shaping **level**, left/right **pan**, frequency space, dynamics, clarity, masking, and headroom. Balance is relational: not every layer should be equally prominent. Ask of Part III's layers: Can each necessary role be heard? Must it be heard continuously? Are kick and bass competing? Does the peak exceed the output range?

The capstone exposes `gain` and `mute`; mono sources make pan intentionally out of scope. Try one change at a time, render, and compare at matched playback level. A future stereo extension could apply constant-power pan, but inventing it here would distract from signal flow.

Objective checks can establish one channel, expected duration/sample rate, valid controls, and peak below one. They cannot prove clarity, emotional effect, or taste. **Software correctness and musical quality overlap, but they are not the same thing.**

The renderer rejects clipping instead of silently normalizing. This keeps excessive summing visible. Headroom is space between typical/peak levels and the maximum representable output; it supports later processing and avoids accidental overload.

## References
See Rumsey and McCormick [30] for mixing and metering practice and Roads [29] for digital signal combination. Subjective questions are presented as listening prompts, not sourced universal rules.
