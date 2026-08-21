# Chapter 262 — Sequence Models

## Model

Music unfolds in order. N-grams and Markov chains use bounded history; recurrent networks carry learned state; transformers use attention over a context. Shuffling tokens destroys timing and causality. Architecture choice changes accessible context and compute; none implies human-like musical understanding.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Müller 2015](../../references/bibliography.md#part-xii-sources); [Bishop 2006](../../references/bibliography.md#part-xii-sources).
