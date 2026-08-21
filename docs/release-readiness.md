# Release readiness — 0.1.0 candidate

Checked on 2026-08-21. A checked item records an actual repository or executable
check; it is not a blanket claim about untested hardware or every external URL.

- [x] Chapter numbering verified: 307 unique, contiguous chapters in Parts I–XII.
- [x] Master TOC generated and verified against every chapter path.
- [x] Internal local Markdown links verified.
- [ ] Every external reference URL manually reverified; source notes retain access limitations.
- [x] Project bibliography inspected for structure and source-note boundaries.
- [x] Glossary and terminology guide added.
- [ ] Every lab manually completed on its target software/hardware.
- [x] Complete automated test suite passing (97 tests).
- [ ] Every part-level capstone manually listened to and visually inspected.
- [x] Generated-output locations ignored and tracked-output policy checked.
- [x] README and master navigation current.
- [x] Contributor/editorial contracts current.
- [x] Version 0.1.0 metadata, changelog, and release notes current.
- [x] Known limitations documented below and in the executable inventory.

## Known limitations

- Ardour/Yoshimi and hardware-dependent labs were not run in the headless audit environment.
- ALSA, JACK, and PipeWire behavior and UI instructions vary by distribution and version.
- Optional machine-learning discussions do not install or verify large ML frameworks.
- External reference availability was not fully network-rechecked; access boundaries remain transparent in source notes.
- Content and code share the repository's existing MIT license; whether that license matches the author's intended long-term publishing model remains an author decision, not a legal conclusion.

## Decision

The repository is a coherent **0.1.0 release candidate**, but this checklist does
not support declaring a final publication-ready edition. Before a public release,
perform the unchecked external-reference, lab, listening, and capstone passes on
representative supported systems.
