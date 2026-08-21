# Chapter 31 — Signal Routing

Routing answers: **where does this signal go next?** A source enters an input, a track may apply an insert, its output reaches a bus or master, and the master reaches output. A **send** branches to another path; a **return** is the processed path coming back. Parallel processing preserves a dry path beside a wet path.

```text
Synth → Synth Track → EQ insert → Main Bus → Master → Output
                         ↘ send → Reverb Bus ↗
```

`routing` in the session JSON is a directed graph. `route_path()` traces reachability; validation checks endpoints, duplicate edges, and whether every track reaches `output`. This educational graph permits shared paths but no feedback is needed. A production DAW may support controlled feedback or impose its own safeguards.

## Follow the signal from source to destination

**Does the source exist? → Does the region contain data? → Is the track active? → Is routing correct? → Is processing passing signal? → Does the bus receive it? → Does the master receive it? → Does output receive it?**

For a silent track, inspect each boundary in order. Do not randomly change plugins. The broken capstone's `orphan` has no route; `route_path(..., "orphan", "output")` returns `None`.

## References
See Rumsey and McCormick [30] for signal flow. Ardour details are intentionally deferred to Chapter 38.
