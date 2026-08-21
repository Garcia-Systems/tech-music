# Chapter 71 — Compression and Audio Codecs

A **codec** defines how audio is encoded/decoded; a **container** organizes encoded data and metadata. Names are sometimes used loosely, so identify both.

| Example | Kind | Loss model | Teaching note |
|---|---|---|---|
| WAV + PCM | RIFF container + PCM encoding | uncompressed | inspectable, not inherently “a codec named WAV” |
| FLAC | codec and native container | lossless | decoded PCM is exact |
| MP3 | compressed audio format | lossy | perceptual data reduction |
| AAC | codec family | lossy (usual profiles) | often carried in MP4 |
| Opus | codec | lossy | designed for interactive and stored audio uses |

**Lossless** compression reconstructs the encoded source sample data exactly; **lossy** coding intentionally discards information according to its model. Bitrate is encoded bits per second and can be constant or variable. It is not bit depth. Container choice alone does not determine quality. Codec algorithms and psychoacoustic internals are intentionally deferred.

## References

- Curtis Roads, *The Computer Music Tutorial*, 2nd ed. (MIT Press, 2023), [bibliography §29](../../references/bibliography.md#29).
- Julius O. Smith III, *Mathematics of the DFT*, 2nd ed. (2007), [bibliography §4](../../references/bibliography.md#4).
- Additional chapter-specific standards and official documentation are indexed in the [Part VI sources](../../references/bibliography.md#part-vi-sources).
