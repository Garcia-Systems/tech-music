# Chapter 100 — Stateful vs Stateless DSP

## Hear → see → describe

Gain is stateless: current output depends only on current input and parameter. Delays, recursive filters, compressors, and envelope followers are stateful: earlier samples live in buffers or variables. Reset is a lifecycle operation, not something to do accidentally.

## Implement, break, debug, verify

Process two different clips with one filter, then with a reset between clips. Decide which behavior the application intends. A reused processor without a deliberate reset can leak history between independent renders.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
