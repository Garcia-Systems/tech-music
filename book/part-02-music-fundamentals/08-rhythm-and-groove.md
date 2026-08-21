# Chapter 8 — Rhythm and Groove

## A grid is a model
**Rhythm** arranges events and rests in musical time. Quarter, eighth, and sixteenth notes conventionally divide a 4/4 bar into 4, 8, and 16 equal notated positions. An **accent** makes an event prominent; **syncopation** emphasizes a normally weaker position or crosses expected boundaries.

```text
Beat:   1 e & a 2 e & a 3 e & a 4 e & a
Kick:   X . . . X . . . X . . . X . . .
Snare:  . . . . X . . . . . . . X . . .
Hat:    X . X . X . X . X . X . X . X .
```

This programmer-friendly grid is one representation, not notation itself. `X` means an onset and `.` a rest. A Boolean list can hold the same information. **Quantization** moves events toward grid positions. **Microtiming** means small timing departures. **Swing** delays alternating subdivisions (often described as unequal pairs); no single percentage defines every performance. **Groove** names an experienced pattern of rhythmic motion and participation, not an algorithmic guarantee.

## Executable and listening lab
In Python, call `step_positions([1,0,1,0,1,0,1,0], 120, 4)`. Compare `swing=0.0` and `swing=0.35`, then make a third list by shifting only one timestamp by 0.015 seconds. Listen without labels first. Record which attacks feel even, loping, or displaced, and whether your description changes after seeing timestamps. Do not treat preference as correctness.

## Debugging an index
If a snare intended for human step 5 is stored at `pattern[5]`, it sounds on the sixth cell because Python indexes from zero. Locate the audible anomaly, print active indices, change only the wrong index, and verify the intended list. This is a temporally incorrect result from valid code.

## Connections
The Part I discussion of groove becomes manipulable event data here. Later, a sequencer will attach sound and velocity to these positions.

## References
See the [bibliography](../../references/bibliography.md): Butler [19] on electronic-dance rhythm and meter; Janata et al. [13] on groove; Frühauf et al. [15] on microtiming; London [25] on meter.
