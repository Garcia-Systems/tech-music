# Part IX capstone debugging solution

1. Graph validation/path inspection finds silence from the disconnected master; reconnect and assert a path.
2. The negative margin identifies a timing miss even though samples are correct; bound or move the work.
3. Comparing timestamps with sample onsets identifies snapping jitter; split the block at event offsets.
4. Endpoint validation names the invalid reference; migrate or repair the durable ID.
5. Comparing a one-block render with a multi-block render exposes reset DSP state; retain phase/delay state across calls.

Verification combines deterministic output comparison with diagnostics. It does not establish actual real-time safety.
