# Chapter 277 — Adaptive Music

## Model

Adaptive music maps application state to musical parameters and playback decisions. Games, installations, exercise tools, and work-session tools can use the pattern `state → music logic → parameters → renderer`. Adaptation is a control design; “focus” is a user-named preset here, not a productivity claim.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Collins 2008](../../references/bibliography.md#part-xii-sources); [Amershi et al. 2019](../../references/bibliography.md#part-xii-sources).
