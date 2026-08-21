# Chapter 253 — Generative Melody

## Model

Unconstrained pitch ignores register and memory. A constrained generator can select scale degrees, favor steps over leaps, keep a range, and occasionally recall a motif. These constraints produce traceable continuity, not guaranteed quality. The capstone logs each step/leap decision and validates pitch membership.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Roads 1996](../../references/bibliography.md#part-xii-sources); [Nierhaus 2009](../../references/bibliography.md#part-xii-sources).
