# Chapter 250 — Grammar and Rule-Based Music

## Model

A grammar separates hierarchical form from event rendering: `TRACK → INTRO BODY OUTRO`; `BODY → A A B A`. Expansion chooses a section tree; later stages schedule phrases and notes. This resembles formal grammar rewriting without requiring a parser or implying that one grammar captures every musical culture.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Roads 1996](../../references/bibliography.md#part-xii-sources); [Nierhaus 2009](../../references/bibliography.md#part-xii-sources).
