# Audio, music, and debugging quick reference

| Quantity | Relationship | Units / condition |
| --- | --- | --- |
| Period | `T = 1 / f` | `T` seconds; `f` hertz, `f > 0` |
| Beat duration | `t_beat = 60 / BPM` | seconds per quarter-note beat; `BPM > 0` |
| Sample interval | `Δt = 1 / f_s` | seconds; sample rate `f_s` in Hz |
| Sample-frame count | `N = duration × f_s` | integer after an explicitly stated rounding policy |
| Nyquist frequency | `f_N = f_s / 2` | Hz; an ideal bound, not an anti-aliasing guarantee |
| Buffer duration | `t_b = B / f_s` | seconds for `B` sample frames |
| DFT-bin spacing | `Δf = f_s / N` | Hz for an `N`-point DFT |
| MIDI 1.0 note frequency | `f = 440 × 2^((n−69)/12)` | Hz; equal temperament with note 69 = A4 |

Common production rates include 44.1 kHz and 48 kHz; higher rates change data
and processing costs and are not automatically better for every purpose. MIDI
1.0 data bytes span 0–127; channel numbering is often displayed as 1–16 even
when program APIs index it as 0–15.

## Diagnostic loop

1. State the **symptom** without guessing its cause.
2. Collect **evidence**: levels, logs, event times, routes, files, plots, or tests.
3. List competing **hypotheses** and test the cheapest discriminating one first.
4. Find the **root cause**, apply one **fix**, and repeat the original observation.
5. Record **verification** and the transferable **engineering lesson**.

For layered silence, trace source → event → processor → route → driver → device →
monitoring. For glitches, measure deadline, block size, scheduling, allocation,
and I/O separately rather than treating “CPU” as one explanation.
