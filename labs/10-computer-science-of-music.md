# Lab 10 — Mini audio engine

Run `python examples/part_09_engine.py`, then inspect the WAV and timing table. Change the block size without changing timestamps; the accurate render should retain onset time. Use `snap_events=True` to expose boundary jitter. Add a processing spike and classify numerical correctness separately from deadline correctness.

## Capstone debugging session

Start with these deliberate faults: remove the route to master; set one simulated processing duration above `buffer_duration`; snap messages to boundaries; reference an unknown node; reset oscillator phase each block. For each, record **Symptom → Evidence → Hypotheses → Investigation → Root Cause → Fix → Verification** using the graph, event timeline, timing rows, tests, and waveform. Never describe this Python exercise as a hardware real-time test.
