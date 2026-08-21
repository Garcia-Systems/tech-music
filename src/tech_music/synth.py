"""Small, dependency-free synthesis building blocks for Part V.

The functions favor visible control flow and validation over production DSP.
Signals are mono floating-point samples in the nominal range -1..1.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Iterable

from .music import midi_to_frequency
from .waveform import write_wav

WAVEFORMS = {"sine", "square", "saw", "triangle"}


def oscillator(frequency: float, duration: float, sample_rate: int = 44_100,
               amplitude: float = 0.5, phase: float = 0.0,
               waveform: str = "sine") -> list[float]:
    """Generate a periodic waveform; ``phase`` is measured in cycles."""
    if frequency <= 0 or duration <= 0 or sample_rate <= 0:
        raise ValueError("frequency, duration, and sample_rate must be positive")
    if frequency >= sample_rate / 2:
        raise ValueError("frequency must be below the Nyquist frequency")
    if not 0 <= amplitude <= 1:
        raise ValueError("amplitude must be between 0 and 1")
    if waveform not in WAVEFORMS:
        raise ValueError(f"unknown waveform: {waveform}")
    result = []
    for n in range(round(duration * sample_rate)):
        cycle = (phase + frequency * n / sample_rate) % 1.0
        if waveform == "sine":
            value = math.sin(2 * math.pi * cycle)
        elif waveform == "square":
            value = 1.0 if cycle < 0.5 else -1.0
        elif waveform == "saw":
            value = 2.0 * cycle - 1.0
        else:
            value = 1.0 - 4.0 * abs(cycle - 0.5)
        result.append(amplitude * value)
    return result


@dataclass(frozen=True)
class ADSR:
    attack: float = 0.01
    decay: float = 0.1
    sustain: float = 0.7
    release: float = 0.2

    def validate(self) -> None:
        if min(self.attack, self.decay, self.release) < 0:
            raise ValueError("ADSR times cannot be negative")
        if not 0 <= self.sustain <= 1:
            raise ValueError("ADSR sustain must be between 0 and 1")


def adsr_envelope(gate_duration: float, envelope: ADSR,
                  sample_rate: int = 44_100) -> list[float]:
    """Return attack/decay/sustain while gated, followed by release to zero."""
    envelope.validate()
    if gate_duration <= 0 or sample_rate <= 0:
        raise ValueError("gate_duration and sample_rate must be positive")
    gate_n = round(gate_duration * sample_rate)
    attack_n = min(gate_n, round(envelope.attack * sample_rate))
    decay_n = min(gate_n - attack_n, round(envelope.decay * sample_rate))
    sustain_n = gate_n - attack_n - decay_n
    attack = ([i / (attack_n - 1) for i in range(attack_n)] if attack_n > 1
              else [1.0] if attack_n else [])
    decay = [1 + (envelope.sustain - 1) * (i + 1) / decay_n
             for i in range(decay_n)] if decay_n else []
    gated = attack + decay + [envelope.sustain] * sustain_n
    release_n = round(envelope.release * sample_rate)
    release_start = gated[-1] if gated else 0.0
    release = [release_start * (1 - (i + 1) / release_n)
               for i in range(release_n)] if release_n else []
    return gated + release


def one_pole_lowpass(samples: Iterable[float], cutoff_hz: float,
                     sample_rate: int = 44_100) -> list[float]:
    """Apply a stable educational one-pole low-pass filter."""
    if sample_rate <= 0 or not 0 < cutoff_hz < sample_rate / 2:
        raise ValueError("cutoff must be between 0 and the Nyquist frequency")
    alpha = 1.0 - math.exp(-2.0 * math.pi * cutoff_hz / sample_rate)
    output, previous = [], 0.0
    for sample in samples:
        previous += alpha * (sample - previous)
        output.append(previous)
    return output


def lfo(rate_hz: float, duration: float, sample_rate: int = 44_100,
        depth: float = 1.0) -> list[float]:
    if rate_hz <= 0 or not 0 <= depth <= 1:
        raise ValueError("LFO rate must be positive and depth must be in 0..1")
    return oscillator(rate_hz, duration, sample_rate, depth, waveform="sine")


def additive_tone(fundamental: float, amplitudes: list[float], duration: float,
                  sample_rate: int = 44_100) -> list[float]:
    """Sum harmonic sine partials and scale only when needed for headroom."""
    if not amplitudes or any(value < 0 for value in amplitudes):
        raise ValueError("provide non-negative harmonic amplitudes")
    components = [oscillator(fundamental * (i + 1), duration, sample_rate,
                             min(1.0, amplitude))
                  for i, amplitude in enumerate(amplitudes) if amplitude]
    total = [sum(values) for values in zip(*components)]
    peak = max((abs(x) for x in total), default=0.0)
    return [x / max(1.0, peak) for x in total]


def fm_tone(carrier_hz: float, modulator_hz: float, depth_hz: float,
            duration: float, sample_rate: int = 44_100,
            amplitude: float = 0.5) -> list[float]:
    """Generate simple sinusoidal FM using depth expressed in hertz."""
    if min(carrier_hz, modulator_hz, duration, sample_rate) <= 0 or depth_hz < 0:
        raise ValueError("FM frequencies/duration must be positive; depth non-negative")
    if carrier_hz + depth_hz >= sample_rate / 2:
        raise ValueError("instantaneous frequency may exceed Nyquist")
    phase, output = 0.0, []
    for n in range(round(duration * sample_rate)):
        instantaneous = carrier_hz + depth_hz * math.sin(2 * math.pi * modulator_hz * n / sample_rate)
        phase += instantaneous / sample_rate
        output.append(amplitude * math.sin(2 * math.pi * phase))
    return output


@dataclass(frozen=True)
class Patch:
    waveform: str
    amplitude: float
    envelope: ADSR
    cutoff_hz: float
    lfo_rate_hz: float = 0.0
    lfo_depth: float = 0.0
    version: int = 1

    @classmethod
    def from_dict(cls, data: dict) -> "Patch":
        required = {"version", "waveform", "amplitude", "amp_envelope", "filter"}
        missing = required - data.keys()
        if missing:
            raise ValueError(f"missing patch parameter(s): {', '.join(sorted(missing))}")
        if data["version"] != 1:
            raise ValueError(f"unsupported patch version: {data['version']}")
        env = ADSR(**data["amp_envelope"])
        patch = cls(data["waveform"], data["amplitude"], env,
                    data["filter"]["cutoff_hz"],
                    data.get("lfo", {}).get("rate_hz", 0.0),
                    data.get("lfo", {}).get("depth", 0.0), data["version"])
        patch.validate()
        return patch

    def validate(self) -> None:
        if self.waveform not in WAVEFORMS:
            raise ValueError(f"unknown waveform: {self.waveform}")
        if not 0 <= self.amplitude <= 1:
            raise ValueError("patch amplitude must be between 0 and 1")
        if self.cutoff_hz <= 0 or self.lfo_rate_hz < 0 or not 0 <= self.lfo_depth <= 1:
            raise ValueError("invalid filter or LFO parameter")
        self.envelope.validate()


def load_patch(path: Path) -> Patch:
    return Patch.from_dict(json.loads(path.read_text(encoding="utf-8")))


@dataclass(frozen=True)
class SynthNote:
    note: int
    start: float
    duration: float
    velocity: float = 1.0


def render_note(note: SynthNote, patch: Patch, sample_rate: int = 44_100) -> list[float]:
    patch.validate()
    if note.start < 0 or note.duration <= 0 or not 0 <= note.velocity <= 1:
        raise ValueError("invalid note event")
    envelope = adsr_envelope(note.duration, patch.envelope, sample_rate)
    frequency = midi_to_frequency(note.note)
    if patch.lfo_rate_hz:
        modulation = lfo(patch.lfo_rate_hz, len(envelope) / sample_rate,
                         sample_rate, patch.lfo_depth)
        phase, tone = 0.0, []
        for amount in modulation:
            phase += frequency * (2.0 ** (amount / 12.0)) / sample_rate
            tone.append(patch.amplitude * math.sin(2 * math.pi * phase) if patch.waveform == "sine"
                        else oscillator(frequency * (2.0 ** (amount / 12.0)), 1 / sample_rate,
                                        sample_rate, patch.amplitude, phase, patch.waveform)[0])
    else:
        tone = oscillator(frequency, len(envelope) / sample_rate, sample_rate,
                          patch.amplitude, waveform=patch.waveform)
    shaped = [sample * level * note.velocity for sample, level in zip(tone, envelope)]
    return one_pole_lowpass(shaped, patch.cutoff_hz, sample_rate)


def render_sequence(patch: Patch, notes: list[SynthNote], sample_rate: int = 44_100) -> list[float]:
    """Render overlapping notes (simple offline polyphony) with peak limiting."""
    if not notes:
        return []
    rendered = [(round(note.start * sample_rate), render_note(note, patch, sample_rate)) for note in notes]
    length = max(start + len(voice) for start, voice in rendered)
    mix = [0.0] * length
    for start, voice in rendered:
        for index, sample in enumerate(voice):
            mix[start + index] += sample
    peak = max(abs(x) for x in mix)
    return [x / max(1.0, peak) for x in mix]


class VoiceManager:
    """Minimal note-on/note-off state model used to teach voice lifecycle."""
    def __init__(self, maximum: int = 8):
        if maximum < 1:
            raise ValueError("maximum voices must be positive")
        self.maximum = maximum
        self.active: list[int] = []

    def note_on(self, note: int) -> None:
        midi_to_frequency(note)
        if note in self.active:
            self.active.remove(note)
        if len(self.active) == self.maximum:
            self.active.pop(0)
        self.active.append(note)

    def note_off(self, note: int) -> None:
        if note in self.active:
            self.active.remove(note)


def render_capstone(patch_path: Path, output_path: Path,
                    sample_rate: int = 22_050) -> list[float]:
    patch = load_patch(patch_path)
    notes = [SynthNote(48, 0.0, .45), SynthNote(55, .5, .45),
             SynthNote(60, 1.0, .45), SynthNote(64, 1.5, .9),
             SynthNote(60, 2.5, .8), SynthNote(64, 2.5, .8), SynthNote(67, 2.5, .8)]
    audio = render_sequence(patch, notes, sample_rate)
    write_wav(output_path, audio, sample_rate)
    return audio
