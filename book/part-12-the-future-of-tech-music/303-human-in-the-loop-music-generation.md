# Chapter 303 — Human-in-the-Loop Music Generation

## Model

`regenerate` supports accept/reject workflows by creating a new seed while optionally locking tempo or events. A UI can expose “keep rhythm,” “change melody,” and parameter edits. The loop is generation → human evaluation → constrained regeneration; history should preserve both rejected and accepted configurations when the user chooses.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Part XII executable model](../../src/tech_music/generative.py); [Roads 1996](../../references/bibliography.md#part-xii-sources).
