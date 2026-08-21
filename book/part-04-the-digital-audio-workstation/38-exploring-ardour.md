# Chapter 38 — Exploring Ardour

Ardour is the intended concrete case study after the general model. Because neither the official site/manual nor an Ardour installation was accessible during this run, the table below is a **verification worksheet**, not a set of published behavior claims. Confirm every term against the official manual version matching the installed application before publication.

| General concept | Ardour case-study term/view |
|---|---|
| project state | session |
| timeline placement | Editor, tracks, regions |
| event/recorded material | MIDI/audio track and region |
| graph nodes and edges | tracks/buses and routing |
| processing component | plugin/processor |
| changing parameter | automation |
| deliverable | export |

Fill the second column from the current official manual during the hands-on run; candidate vocabulary is supplied only to guide what to verify. Menu paths are intentionally omitted.

## Hands-on lab (documented, not executed here)

Ardour was **not installed** in the audit environment. Using the current official manual for your installed version:

1. Create a session at the intended sample rate; add MIDI/audio tracks, one bus, and master.
2. Import a generated Part III WAV. Create a short MIDI region and select a locally available instrument.
3. Place regions at section boundaries and verify them in the Editor.
4. Route both tracks to master; send to the bus and add an available effect. Confirm dry/wet paths.
5. Automate gain, bypass/re-enable the effect, and follow the complete signal path.
6. Export the marked range to WAV; inspect duration, rate, channels, and peak.

Record Ardour version, manual date, audio backend, installed plugins, and observed labels. These are reproducible instructions, not claims of execution.

## References
Official Ardour project/manual [32] is recorded as an **uninspected source target, not cited evidence**. Network inspection was attempted but blocked by the environment proxy on 2026-08-21; no behavior or menu claim is attributed to it. See the [source note](../../references/source-notes/part-04.md).
