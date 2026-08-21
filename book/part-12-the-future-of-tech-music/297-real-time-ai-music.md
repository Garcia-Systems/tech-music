# Chapter 297 — Real-Time AI Music

## Model

Offline generation may take longer than playback; near-real-time must remain usefully responsive; a real-time callback must meet every buffer deadline. Generate ahead, bound work, keep network calls off audio threads, and define behavior on misses. Musical deadlines reconnect directly to Part IX scheduling.

## Engineering questions

- What inputs, state, parameters, and versions determine the result?
- Which decision is fixed, sampled, learned, or left to a person?
- What invariant can software test, and what judgment requires a listener?
- What failure evidence and recovery control should the interface expose?

## Connection to the book

Parts II and VIII supply musical/event vocabulary; Parts V–VII render and process sound; Parts IX–XI supply scheduling, persistence, validation, and hardware boundaries.

## References

- [U.S. Copyright Office 2025](../../references/bibliography.md#part-xii-sources); [NIST AI RMF](../../references/bibliography.md#part-xii-sources); [Amershi et al. 2019](../../references/bibliography.md#part-xii-sources).
