# Chapter 91 — Convolution

## Hear → see → describe

Discrete convolution is `y[n] = Σ_k x[k] h[n-k]`. `x` is input, `h` is a kernel/impulse response, and each output sample is a multiply-and-sum over aligned shifts. For `x=[1,2,0]`, `h=[1,0.5]`: `y[0]=1`, `y[1]=0.5+2=2.5`, `y[2]=1`, `y[3]=0`.

## Implement, break, debug, verify

Run the direct nested-loop implementation and compare it within tolerance to a trusted implementation when available. Output length is `len(x)+len(h)-1`. **Boundary bug:** allocating one fewer sample loses the tail; verify the manual example.

```bash
python examples/part_07_dsp.py
pytest -q tests/test_dsp.py
```

## References

- Smith, Julius O., *Introduction to Digital Filters with Audio Applications* [bibliography entry 34](../../references/bibliography.md#34).
- Smith, Julius O., *Mathematics of the DFT* [bibliography entry 4](../../references/bibliography.md).
- Lyons, Richard G., *Understanding Digital Signal Processing*, 3rd ed. [bibliography entry 42](../../references/bibliography.md#42).
