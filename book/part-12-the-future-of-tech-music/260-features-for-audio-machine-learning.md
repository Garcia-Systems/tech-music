# Chapter 260 — Features for Audio Machine Learning

![Chapter 260](../../images/chapters/260.png)

## Model

RMS summarizes energy; zero-crossing rate counts sign changes; spectral centroid is an energy-weighted frequency center; rolloff locates a chosen cumulative spectral proportion; MFCCs compact a perceptually motivated spectral envelope. Sine, saw, and noise differ in these measures, though no single feature identifies a sound reliably.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [Müller 2015](../../references/bibliography.md#part-xii-sources); [Bishop 2006](../../references/bibliography.md#part-xii-sources).
