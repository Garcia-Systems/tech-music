# Part VIII Capstone Debugging — Where Does the Event Stop?

Construct a broken sequence with: note 200; a note-on lacking note-off; an event
on an unmapped channel; 480 ticks treated as seconds; CC 3 mapped to nonexistent
`brightness`; and a retrigger whose note-on is processed before note-off.

Do not fix everything at once. For each symptom preserve evidence and record
**Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix →
Verification**.

Required evidence includes the raw event list, values with units, validation
errors, sorted scheduler log, routing table, piano roll, active synth voices, and
a focused test. Finish only when all events validate, every note lifecycle closes,
all destinations/controls exist, timing matches hand calculations, ordering is
deterministic, and the rendered duration is expected.

Compare with the [solution](../solutions/part-08-capstone-debugging.md) only after
recording your hypotheses.
