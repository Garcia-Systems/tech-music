"""Transparent generative and adaptive music models used by Part XII.

This module is deliberately dependency-free.  It models decisions as data and uses
the existing Part IX ``Session``/``MiniEngine`` renderer; it is not an AI model.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import json
import math
import random
from typing import Iterable, Mapping, Sequence

from .engine import Message, MiniEngine, Session


MODES = {
    "focus": {"tempo": (92, 108), "density": .45, "variation": .12, "patch": "soft-sine"},
    "deep-focus": {"tempo": (72, 92), "density": .32, "variation": .06, "patch": "soft-sine"},
    "light-work": {"tempo": (100, 120), "density": .58, "variation": .20, "patch": "round-triangle"},
    "break": {"tempo": (78, 104), "density": .35, "variation": .28, "patch": "round-triangle"},
    "exploration": {"tempo": (108, 132), "density": .70, "variation": .42, "patch": "bright-saw"},
}
SAFE_PATCHES = frozenset({"soft-sine", "round-triangle", "bright-saw"})
SCALES = {"major": (0, 2, 4, 5, 7, 9, 11), "minor": (0, 2, 3, 5, 7, 8, 10),
          "pentatonic": (0, 2, 4, 7, 9)}


@dataclass(frozen=True, order=True)
class NoteEvent:
    start: float
    duration: float
    note: int
    velocity: float = .7
    layer: str = "melody"

    def validate(self, maximum_time: float) -> None:
        if self.start < 0 or self.duration <= 0 or self.start + self.duration > maximum_time + 1e-9:
            raise ValueError("event must fit inside the requested duration")
        if not 0 <= self.note <= 127 or not 0 <= self.velocity <= 1:
            raise ValueError("note and velocity must be valid MIDI values")


@dataclass(frozen=True)
class AdaptiveConfig:
    mode: str = "focus"
    duration: float = 8.0
    tempo_min: int = 92
    tempo_max: int = 108
    density: float | None = None
    variation: float | None = None
    root: int = 60
    scale: str = "minor"
    seed: int = 0
    schema_version: int = 1

    def validate(self) -> None:
        if self.mode not in MODES: raise ValueError(f"unknown mode: {self.mode}")
        if not 0 < self.duration <= 3600: raise ValueError("duration must be in (0, 3600]")
        if not 30 <= self.tempo_min <= self.tempo_max <= 300: raise ValueError("invalid tempo range")
        if self.scale not in SCALES: raise ValueError(f"unknown scale: {self.scale}")
        if not 0 <= self.root <= 127: raise ValueError("root must be a MIDI note")
        for name, value in (("density", self.density), ("variation", self.variation)):
            if value is not None and not 0 <= value <= 1: raise ValueError(f"{name} must be in 0..1")
        if self.schema_version != 1: raise ValueError("unsupported configuration schema")

    def to_json(self) -> str:
        self.validate(); return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "AdaptiveConfig":
        value = cls(**json.loads(text)); value.validate(); return value


@dataclass(frozen=True)
class Generation:
    config: AdaptiveConfig
    tempo: int
    patch: str
    sections: tuple[dict, ...]
    events: tuple[NoteEvent, ...]
    decisions: tuple[str, ...]


def weighted_choice(rng: random.Random, choices: Mapping[object, float]):
    """Choose after validating finite, non-negative weights (normalization is implicit)."""
    if not choices or any(not math.isfinite(w) or w < 0 for w in choices.values()):
        raise ValueError("weights must be finite and non-negative")
    total = sum(choices.values())
    if total <= 0: raise ValueError("at least one weight must be positive")
    point = rng.random() * total
    for item, weight in choices.items():
        point -= weight
        if point < 0: return item
    return next(reversed(choices))


def markov_sequence(transitions: Mapping[str, Mapping[str, float]], start: str,
                    length: int, seed: int) -> list[str]:
    if length < 1 or start not in transitions: raise ValueError("invalid Markov start or length")
    rng, result = random.Random(seed), [start]
    while len(result) < length:
        state = result[-1]
        if state not in transitions: raise ValueError(f"missing transition state: {state}")
        result.append(str(weighted_choice(rng, transitions[state])))
    return result


def euclidean_pattern(pulses: int, steps: int) -> tuple[int, ...]:
    """Evenly distribute pulses with the accumulator form of a Euclidean rhythm."""
    if steps < 1 or not 0 <= pulses <= steps: raise ValueError("require 0 <= pulses <= steps")
    bucket, result = 0, []
    for _ in range(steps):
        bucket += pulses
        if bucket >= steps: bucket -= steps; result.append(1)
        else: result.append(0)
    return tuple(result)


def encode_events(events: Iterable[NoteEvent]) -> list[str]:
    tokens = []
    for event in sorted(events):
        tokens.extend((f"TIME_{event.start:.3f}", f"NOTE_{event.note}",
                       f"DUR_{event.duration:.3f}", f"VEL_{event.velocity:.3f}", f"LAYER_{event.layer}"))
    return tokens


def decode_events(tokens: Sequence[str]) -> list[NoteEvent]:
    if len(tokens) % 5: raise ValueError("each event requires five tokens")
    result = []
    for i in range(0, len(tokens), 5):
        fields = tokens[i:i + 5]
        expected = ("TIME_", "NOTE_", "DUR_", "VEL_", "LAYER_")
        if any(not value.startswith(prefix) for value, prefix in zip(fields, expected)):
            raise ValueError("invalid token order")
        result.append(NoteEvent(float(fields[0][5:]), float(fields[2][4:]), int(fields[1][5:]),
                                float(fields[3][4:]), fields[4][6:]))
    return result


def generate(config: AdaptiveConfig) -> Generation:
    config.validate(); preset = MODES[config.mode]; rng = random.Random(config.seed)
    low, high = max(config.tempo_min, preset["tempo"][0]), min(config.tempo_max, preset["tempo"][1])
    if low > high: raise ValueError("tempo preference does not overlap the mode range")
    tempo = rng.randint(low, high); density = preset["density"] if config.density is None else config.density
    variation = preset["variation"] if config.variation is None else config.variation
    beat = 60 / tempo; step = beat / 2; scale = SCALES[config.scale]
    section_names = ("intro", "body", "outro")
    section_length = config.duration / len(section_names)
    sections = tuple({"section": name, "start": round(i * section_length, 6),
                      "layers": ["pulse"] + (["melody"] if i == 1 else [])}
                     for i, name in enumerate(section_names))
    events, decisions, last_degree = [], [], 0
    t = 0.0
    while t + min(.08, step * .75) <= config.duration + 1e-9:
        if rng.random() < density:
            leap = rng.random() < variation
            delta = rng.choice((-2, 2)) if leap else rng.choice((-1, 0, 1))
            last_degree = max(0, min(len(scale) - 1, last_degree + delta))
            note = config.root + scale[last_degree]
            duration = min(step * .75, config.duration - t)
            event = NoteEvent(round(t, 9), duration, note, .55 + .25 * rng.random())
            event.validate(config.duration); events.append(event)
            decisions.append(f"t={t:.3f}: degree {last_degree}; {'leap' if leap else 'step'}")
        t += step
    return Generation(config, tempo, str(preset["patch"]), sections, tuple(sorted(events)), tuple(decisions))


def regenerate(generation: Generation, *, lock_tempo: bool = False,
               lock_events: bool = False, seed: int | None = None) -> Generation:
    candidate = generate(replace(generation.config, seed=generation.config.seed + 1 if seed is None else seed))
    return replace(candidate, tempo=generation.tempo if lock_tempo else candidate.tempo,
                   events=generation.events if lock_events else candidate.events)


def to_session(generation: Generation, sample_rate: int = 8000) -> Session:
    messages = []
    order = 0
    for event in generation.events:
        start, end = round(event.start * sample_rate), round((event.start + event.duration) * sample_rate)
        messages += [Message(start, order, "note_on", {"note": event.note, "velocity": event.velocity}),
                     Message(end, order + 1, "note_off", {"note": event.note})]
        order += 2
    duration_frames = round(generation.config.duration * sample_rate) + 1
    session = Session(sample_rate, 128, duration_frames, sorted(messages), .22)
    if errors := session.validate(): raise ValueError("; ".join(errors))
    return session


def render(generation: Generation, sample_rate: int = 8000) -> list[float]:
    audio = MiniEngine(to_session(generation, sample_rate)).render()
    if any(not math.isfinite(x) for x in audio) or max(map(abs, audio), default=0) > 1:
        raise ValueError("unsafe generated audio")
    return audio
