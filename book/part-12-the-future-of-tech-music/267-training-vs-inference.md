# Chapter 267 — Training vs Inference

## Model

**Training** adjusts model parameters from data and a loss. **Inference** holds those parameters fixed while producing a prediction or generation from new context. Training normally needs datasets, optimization state, and evaluation; inference needs a versioned model, preprocessing contract, sampling configuration, and validated output.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Vaswani et al. 2017](../../references/bibliography.md#part-xii-sources); [Copet et al. 2023](../../references/bibliography.md#part-xii-sources); [Ho et al. 2020](../../references/bibliography.md#part-xii-sources).
