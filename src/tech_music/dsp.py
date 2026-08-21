"""Readable, dependency-free DSP models for Part VII.

Samples are normalized ``float`` values.  Processors do not silently clamp:
callers can measure an unsafe signal before PCM export clips it.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from typing import Iterable


def gain(samples: Iterable[float], value: float) -> list[float]:
    if not math.isfinite(value):
        raise ValueError("gain must be finite")
    return [value * sample for sample in samples]


def mix(*signals: Iterable[float]) -> list[float]:
    values = [list(signal) for signal in signals]
    if not values:
        return []
    if len({len(signal) for signal in values}) != 1:
        raise ValueError("signals must have equal lengths")
    return [sum(frame) for frame in zip(*values)]


def peak(samples: Iterable[float]) -> float:
    return max((abs(value) for value in samples), default=0.0)


def rms(samples: Iterable[float]) -> float:
    values = list(samples)
    return math.sqrt(sum(value * value for value in values) / len(values)) if values else 0.0


def delay_samples(milliseconds: float, sample_rate: int) -> int:
    if milliseconds < 0 or not math.isfinite(milliseconds) or sample_rate <= 0:
        raise ValueError("milliseconds must be finite/non-negative and rate positive")
    return int(math.floor(milliseconds * sample_rate / 1000.0 + 0.5))


def pure_delay(samples: Iterable[float], delay: int) -> list[float]:
    values = list(samples)
    if delay < 0:
        raise ValueError("delay must be non-negative")
    return [0.0] * delay + values


@dataclass
class FeedbackDelay:
    delay: int
    feedback: float
    mix: float = 0.5

    def __post_init__(self) -> None:
        if self.delay < 1 or not -1 < self.feedback < 1 or not 0 <= self.mix <= 1:
            raise ValueError("delay >= 1, abs(feedback) < 1, and mix in [0, 1] required")
        self._buffer = [0.0] * self.delay
        self._position = 0

    def process(self, samples: Iterable[float]) -> list[float]:
        output = []
        for sample in samples:
            delayed = self._buffer[self._position]
            self._buffer[self._position] = sample + self.feedback * delayed
            self._position = (self._position + 1) % self.delay
            output.append((1 - self.mix) * sample + self.mix * delayed)
        return output

    def reset(self) -> None:
        self._buffer[:] = [0.0] * self.delay
        self._position = 0


@dataclass
class OnePoleLowPass:
    alpha: float
    state: float = 0.0

    def __post_init__(self) -> None:
        if not 0 < self.alpha <= 1 or not math.isfinite(self.alpha):
            raise ValueError("alpha must be finite and in (0, 1]")

    @classmethod
    def from_cutoff(cls, cutoff_hz: float, sample_rate: int) -> "OnePoleLowPass":
        if not 0 < cutoff_hz < sample_rate / 2:
            raise ValueError("cutoff must lie between 0 Hz and Nyquist")
        return cls(1 - math.exp(-2 * math.pi * cutoff_hz / sample_rate))

    def process(self, samples: Iterable[float]) -> list[float]:
        output = []
        for sample in samples:
            self.state += self.alpha * (sample - self.state)
            output.append(self.state)
        return output

    def reset(self) -> None:
        self.state = 0.0


def high_pass(samples: Iterable[float], alpha: float) -> list[float]:
    values = list(samples)
    low = OnePoleLowPass(alpha).process(values)
    return [sample - low_sample for sample, low_sample in zip(values, low)]


def hard_clip(samples: Iterable[float], limit: float = 1.0) -> list[float]:
    if not 0 < limit <= 1:
        raise ValueError("limit must be in (0, 1]")
    return [max(-limit, min(limit, sample)) for sample in samples]


def soft_clip(samples: Iterable[float], drive: float = 1.0) -> list[float]:
    if drive <= 0 or not math.isfinite(drive):
        raise ValueError("drive must be finite and positive")
    scale = math.tanh(drive)
    return [math.tanh(drive * sample) / scale for sample in samples]


def envelope(samples: Iterable[float], attack_ms: float, release_ms: float,
             sample_rate: int) -> list[float]:
    if attack_ms <= 0 or release_ms <= 0 or sample_rate <= 0:
        raise ValueError("times and sample rate must be positive")
    attack = math.exp(-1 / (attack_ms * sample_rate / 1000))
    release = math.exp(-1 / (release_ms * sample_rate / 1000))
    state, output = 0.0, []
    for sample in samples:
        target = abs(sample)
        coefficient = attack if target > state else release
        state = coefficient * state + (1 - coefficient) * target
        output.append(state)
    return output


def compress(samples: Iterable[float], threshold: float, ratio: float,
             attack_ms: float, release_ms: float, sample_rate: int,
             makeup: float = 1.0) -> list[float]:
    values = list(samples)
    if not 0 < threshold <= 1 or ratio < 1 or makeup < 0:
        raise ValueError("threshold in (0,1], ratio >= 1, makeup >= 0 required")
    levels = envelope(values, attack_ms, release_ms, sample_rate)
    output = []
    for sample, level in zip(values, levels):
        desired = level if level <= threshold else threshold + (level - threshold) / ratio
        output.append(sample * (desired / level if level else 1.0) * makeup)
    return output


def convolve(signal: Iterable[float], kernel: Iterable[float]) -> list[float]:
    x, h = list(signal), list(kernel)
    if not x or not h:
        return []
    output = [0.0] * (len(x) + len(h) - 1)
    for k, sample in enumerate(x):
        for j, coefficient in enumerate(h):
            output[k + j] += sample * coefficient
    return output


def dft(samples: Iterable[float]) -> list[complex]:
    values = list(samples)
    size = len(values)
    return [sum(sample * cmath.exp(-2j * math.pi * k * n / size)
                for n, sample in enumerate(values)) for k in range(size)] if size else []


def frequency_bins(size: int, sample_rate: int) -> list[float]:
    if size <= 0 or sample_rate <= 0:
        raise ValueError("size and sample rate must be positive")
    return [index * sample_rate / size for index in range(size)]


def hann(size: int) -> list[float]:
    if size < 1:
        raise ValueError("size must be positive")
    return [1.0] if size == 1 else [0.5 - 0.5 * math.cos(2 * math.pi * n / (size - 1)) for n in range(size)]


def process_blocks(processor: object, samples: Iterable[float], block_size: int) -> list[float]:
    if block_size <= 0:
        raise ValueError("block size must be positive")
    values, output = list(samples), []
    for start in range(0, len(values), block_size):
        output.extend(processor.process(values[start:start + block_size]))
    return output


class DSPRack:
    """A deterministic offline rack built from an educational configuration."""

    def __init__(self, processors: list[dict], sample_rate: int):
        if sample_rate <= 0:
            raise ValueError("sample rate must be positive")
        self.sample_rate = sample_rate
        self.configuration = processors
        self.stages: list[tuple[dict, object | None]] = []
        for config in processors:
            kind = config.get("type")
            if kind == "gain":
                if not math.isfinite(config.get("value", math.nan)):
                    raise ValueError("gain value required")
                stage = None
            elif kind == "lowpass":
                stage = OnePoleLowPass.from_cutoff(config.get("cutoff_hz", 0), sample_rate)
            elif kind == "distortion":
                if config.get("drive", 0) <= 0:
                    raise ValueError("positive distortion drive required")
                stage = None
            elif kind == "delay":
                stage = FeedbackDelay(delay_samples(config.get("milliseconds", -1), sample_rate),
                                      config.get("feedback", 0), config.get("mix", 0.25))
            else:
                raise ValueError(f"unknown processor type: {kind!r}")
            self.stages.append((config, stage))

    def process(self, samples: Iterable[float]) -> list[float]:
        output = list(samples)
        for config, stage in self.stages:
            if config.get("bypass", False):
                continue
            kind = config["type"]
            if kind == "gain":
                output = gain(output, config["value"])
            elif kind == "lowpass":
                output = stage.process(output)  # type: ignore[union-attr]
            elif kind == "distortion":
                output = soft_clip(output, config["drive"])
            else:
                output = stage.process(output)  # type: ignore[union-attr]
        return output

    def diagnostics(self, source: Iterable[float], output: Iterable[float]) -> dict:
        source_values, output_values = list(source), list(output)
        return {"sample_rate": self.sample_rate, "frames": len(output_values),
                "input_peak": peak(source_values), "output_peak": peak(output_values),
                "input_rms": rms(source_values), "output_rms": rms(output_values),
                "clipping": peak(output_values) > 1.0,
                "processors": [{**config, "bypassed": config.get("bypass", False)}
                               for config, _ in self.stages]}
