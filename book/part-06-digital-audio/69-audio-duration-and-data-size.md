# Chapter 69 — Audio Duration and Data Size

For uncompressed PCM:

`data_rate_bits_per_second = sample_rate × bit_depth × channels`

`pcm_data_size_bytes = duration × sample_rate × bit_depth × channels / 8`

At 48,000 samples/s, 16 bits/sample, stereo: `48,000 × 16 × 2 = 1,536,000 bit/s = 192,000 byte/s`. Units cancel visibly. A 60-second stream has 11,520,000 PCM data bytes. A container adds headers/chunks, so total file size is generally larger; padding or metadata may add more.

The executable `pcm_data_size` first turns duration into an integer frame count using the documented rounding rule, then multiplies by bytes per frame. It rejects non-whole-byte teaching depths. Compare mono/stereo, rates, depths, and durations in a Python shell. Tests verify 8-bit mono and 16-bit stereo cases.

**Units debug rule:** bits are not bytes; bit depth is bits/sample, while bitrate is bits/second. Channels is a multiplier, not a unit of time.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), [bibliography §29](../../references/bibliography.md#29).
- Julius O. Smith III, *Mathematics of the DFT*, 2nd ed. (2007), [bibliography §4](../../references/bibliography.md#4).
- Additional chapter-specific standards and official documentation are indexed in the [Part VI sources](../../references/bibliography.md#part-vi-sources).
