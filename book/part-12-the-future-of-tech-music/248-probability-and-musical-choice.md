# Chapter 248 — Probability and Musical Choice

## Model

A distribution can encode “repeat .70, vary .20, rest .10.” Weights need not already sum to one if the implementation explicitly normalizes, but they must be finite, non-negative, and have a positive total. Count outcomes over many seeded trials to inspect implementation behavior; sampling noise means small runs need tolerances.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Roads 1996](../../references/bibliography.md#part-xii-sources); [Nierhaus 2009](../../references/bibliography.md#part-xii-sources).
