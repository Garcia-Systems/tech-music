# Chapter 278 — Interactive Music Systems

## Model

Inputs can be actions, sensors, application events, time, or streams. Normalize them into typed events, update a state machine, then schedule musical changes safely. FOCUS, BREAK, ALERT, and COMPLETE should map explicitly to tempo/density/variation rather than hiding behavior in conditionals.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Collins 2008](../../references/bibliography.md#part-xii-sources); [Amershi et al. 2019](../../references/bibliography.md#part-xii-sources).
