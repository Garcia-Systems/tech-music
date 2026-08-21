"""Small, dependency-free digital-audio models used by Part VI.

The functions favor explicit units and inspectable PCM WAV files over a broad
media API.  They are educational building blocks, not a production decoder.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import math
import struct
import wave


def sample_count(duration_seconds: float, sample_rate: int) -> int:
    """Return a nearest-integer frame count; reject nonsensical inputs."""
    if duration_seconds < 0 or sample_rate <= 0:
        raise ValueError("duration must be non-negative and sample_rate positive")
    return int(math.floor(duration_seconds * sample_rate + 0.5))


def sample_interval(sample_rate: int) -> float:
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    return 1.0 / sample_rate


def nyquist_frequency(sample_rate: int) -> float:
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    return sample_rate / 2.0


def buffer_duration_ms(buffer_size: int, sample_rate: int) -> float:
    if buffer_size < 0:
        raise ValueError("buffer_size must be non-negative")
    return 1000.0 * buffer_size * sample_interval(sample_rate)


def pcm_data_size(duration_seconds: float, sample_rate: int,
                  bit_depth: int, channels: int) -> int:
    if bit_depth <= 0 or bit_depth % 8 or channels <= 0:
        raise ValueError("bit_depth must be positive whole bytes; channels positive")
    return sample_count(duration_seconds, sample_rate) * channels * bit_depth // 8


def float_to_pcm16(value: float, *, clip: bool = True) -> int:
    """Map normalized float to signed PCM16, preserving both endpoints."""
    if not math.isfinite(value):
        raise ValueError("sample must be finite")
    if not clip and not -1.0 <= value <= 1.0:
        raise ValueError("sample outside normalized range")
    value = max(-1.0, min(1.0, value))
    return -32768 if value <= -1.0 else int(round(value * 32767))


def pcm16_to_float(value: int) -> float:
    if not -32768 <= value <= 32767:
        raise ValueError("value outside PCM16 range")
    return value / (32768.0 if value < 0 else 32767.0)


def interleave(*channels: list[int]) -> list[int]:
    if not channels or len({len(channel) for channel in channels}) != 1:
        raise ValueError("one or more equally sized channels required")
    return [sample for frame in zip(*channels) for sample in frame]


def sine(frequency: float, duration_seconds: float, sample_rate: int,
         amplitude: float = 0.5, phase: float = 0.0) -> list[float]:
    if frequency < 0 or not 0 <= amplitude <= 1:
        raise ValueError("frequency and amplitude must be in valid ranges")
    return [amplitude * math.sin(2 * math.pi * frequency * n / sample_rate + phase)
            for n in range(sample_count(duration_seconds, sample_rate))]


def quantize(samples: list[float], bit_depth: int) -> list[float]:
    """Educational signed symmetric quantizer returned as normalized floats."""
    if bit_depth < 2 or bit_depth > 24:
        raise ValueError("educational bit depth must be 2..24")
    maximum = 2 ** (bit_depth - 1) - 1
    minimum = -(2 ** (bit_depth - 1))
    result = []
    for value in samples:
        value = max(-1.0, min(1.0, value))
        integer = minimum if value <= -1 else round(value * maximum)
        result.append(integer / (abs(minimum) if integer < 0 else maximum))
    return result


def write_pcm16(path: str | Path, channels: list[list[float]], sample_rate: int) -> Path:
    if not channels or len({len(c) for c in channels}) != 1:
        raise ValueError("one or more equally sized channels required")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    values = interleave(*[[float_to_pcm16(v) for v in c] for c in channels])
    with wave.open(str(path), "wb") as output:
        output.setparams((len(channels), 2, sample_rate, len(channels[0]), "NONE", "not compressed"))
        output.writeframes(struct.pack(f"<{len(values)}h", *values))
    return path


@dataclass(frozen=True)
class AudioReport:
    path: str
    sample_rate: int
    channels: int
    frames: int
    sample_values: int
    duration_seconds: float
    sample_representation: str
    peak_amplitude: float
    clipping: bool
    pcm_data_bytes: int


def inspect_wav(path: str | Path) -> AudioReport:
    """Inspect uncompressed 8- or 16-bit PCM WAV using only the standard library."""
    path = Path(path)
    with wave.open(str(path), "rb") as source:
        channels, width, rate, frames = (source.getnchannels(), source.getsampwidth(),
                                          source.getframerate(), source.getnframes())
        if source.getcomptype() != "NONE" or width not in (1, 2):
            raise ValueError("inspector supports uncompressed 8/16-bit PCM WAV only")
        raw = source.readframes(frames)
    if width == 1:
        normalized = [(v - 128) / (128.0 if v < 128 else 127.0) for v in raw]
        representation = "unsigned 8-bit PCM"
    else:
        values = struct.unpack(f"<{len(raw) // 2}h", raw)
        normalized = [pcm16_to_float(v) for v in values]
        representation = "signed 16-bit little-endian PCM"
    peak = max(map(abs, normalized), default=0.0)
    return AudioReport(str(path), rate, channels, frames, frames * channels,
                       frames / rate, representation, peak, peak >= 1.0, len(raw))


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect an uncompressed PCM WAV file")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    for key, value in asdict(inspect_wav(args.path)).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
