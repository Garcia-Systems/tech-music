# Chapter 55 — Polyphony and Voice Management

A monophonic instrument maintains one sounding note; a polyphonic instrument maintains multiple **voices**, each with oscillator/envelope/filter state. Note-on allocates or retriggers; note-off moves a matching voice toward release. When capacity is full, a policy may steal a voice.

`VoiceManager` models state, not audio. It steals the oldest active note. `render_sequence` provides offline polyphony by placing complete voices on a shared timeline. Play `polyphonic-chord.wav`: three notes require three concurrent voice signals, not one oscillator somehow holding three frequencies.

**Debug lab.** Delete the removal in `note_off`. The active set retains the note: a stuck voice. Assert lifecycle after every event. Production systems also distinguish repeated note IDs/channels; this deliberately minimal model does not.

## References
See Roads [29] and RFC 8259 [33] where JSON serialization is discussed.
