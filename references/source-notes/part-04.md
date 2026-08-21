# Part IV source inspection note

- **Date / inspector:** 2026-08-21 / Codex
- **Stable sources inspected in the repository audit:** Roads, *The Computer Music Tutorial*, 2nd ed. publisher record already inspected for Part III; Python `wave` documentation already inspected for the executable WAV contract; existing Part III code/data/artifacts and project research standard.
- **Additional stable bibliographic sources selected:** Rumsey and McCormick, *Sound and Recording*, 7th ed.; Steinberg VST 3 Developer Portal; RFC 8259 (JSON).
- **Ardour official sources targeted:** Ardour project site and current online Ardour Manual sections for sessions, Editor, tracks, regions, MIDI, routing, plugins, automation, mixer, and export.
- **Inspection result:** direct HTTPS attempts to `manual.ardour.org` and the official manual repository returned `CONNECT tunnel failed, response 403`; the web research service returned 401. Ardour was not installed. Consequently Chapter 38 states this limitation, avoids menu paths/version-dependent gestures, and confines mapping to stable project vocabulary. These pages must be re-inspected against the installed/current version before publication.
- **Claim limits:** the JSON schema, renderer, delay, validation rules, and diagrams are educational project designs—not claims about Ardour internals or file format. General concepts are separated from the Ardour case study.
