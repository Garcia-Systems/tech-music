# Chapter 87 — Dynamic Range and Compression

## Hear → see → describe

A compressor reduces level above a threshold. Ratio describes input change to output change; attack and release are time constants in milliseconds; gain reduction changes level, and makeup gain follows. Compression is a choice, not an automatic improvement.

## Implement, break, debug, verify

The executable model follows absolute peak level, then applies a simplified linear-amplitude transfer. Inspect `compression-envelope.svg`. **Break it:** pass milliseconds as seconds. Sluggish or pumping control suggests a units fault; verify coefficient calculations and a stepped test signal.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
