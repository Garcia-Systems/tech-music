# Terminology guide

Use **sound** for a physical acoustic event, **audio signal** for a varying
physical or numerical representation, and **digital audio data** for encoded
samples plus the metadata needed to interpret them. A **sample** is one channel's
value at an instant; a **sample frame** contains simultaneous values for every
audio channel.

An **audio channel** is one signal path, a **MIDI channel** is a numbered routing
and addressing field, and a **DAW track** is an arrangement and processing
container that may carry audio or musical events. Do not use these interchangeably.

Use **MIDI event** only for data conforming to a MIDI protocol or file. Use
**musical event** or **note event** for a program's generic representation. A
**buffer** is storage; a processing **block** is the group of frames handled in
one operation; a **callback** is the function invoked under the audio system's
deadline.

A **processor** transforms a signal. A **plugin** is a loadable component that
implements a host contract. A **bus** combines or distributes signals; a
**send** routes a copy toward another path and a **return** receives that path.
Use **render** for computing an output and **export** for the user-facing act of
writing a deliverable. A **generated artifact** is reproducible output, never the
source program or required hand-authored teaching asset.

For oscillator, voice, patch, preset, envelope, track, sequencer, and other
reader-facing definitions, use the [glossary](glossary.md).
