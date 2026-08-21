"""Readable, deterministic MIDI/event models for Part VIII.

This is an offline teaching sequencer, not a complete MIDI protocol stack.  Times
are integer ticks until scheduling; audio is a separate list of float samples.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import math
from pathlib import Path
import struct
from typing import Iterable, Mapping

from .music import midi_to_frequency
from .synth import ADSR, Patch, SynthNote, render_sequence

EVENT_PRIORITY = {"program_change": 0, "control_change": 1, "pitch_bend": 2,
                  "note_off": 3, "note_on": 4}


@dataclass(frozen=True)
class MidiEvent:
    tick: int
    type: str
    channel: int = 0                 # API convention: MIDI 1.0 channels 0..15
    note: int | None = None
    velocity: int | None = None
    controller: int | None = None
    value: int | None = None
    bend: int | None = None          # signed, centered at 0: -8192..8191
    track: int = 0
    order: int = 0                   # stable source order tie-breaker


@dataclass(frozen=True)
class TempoEvent:
    tick: int
    bpm: float


@dataclass(frozen=True)
class ScheduledEvent:
    seconds: float
    event: MidiEvent


def validate_event(event: MidiEvent, destinations: Iterable[int] | None = None) -> None:
    """Reject unsupported/invalid data rather than silently repairing it."""
    if event.type not in EVENT_PRIORITY:
        raise ValueError(f"Invalid MIDI event: unrecognized type={event.type!r}")
    if event.tick < 0:
        raise ValueError(f"Invalid MIDI event: tick={event.tick} must be nonnegative")
    if not 0 <= event.channel <= 15:
        raise ValueError(f"Invalid MIDI event: channel={event.channel} is outside 0..15")
    if event.type in {"note_on", "note_off"}:
        if event.note is None or not 0 <= event.note <= 127:
            raise ValueError(f"Invalid note event: note={event.note} exceeds supported MIDI note range 0..127")
        if event.velocity is None or not 0 <= event.velocity <= 127:
            raise ValueError(f"Invalid note event: velocity={event.velocity} is outside 0..127")
    if event.type == "control_change":
        if event.controller is None or not 0 <= event.controller <= 127:
            raise ValueError("Invalid control change: controller must be in 0..127")
        if event.value is None or not 0 <= event.value <= 127:
            raise ValueError("Invalid control change: value must be in 0..127")
    if event.type == "pitch_bend" and (event.bend is None or not -8192 <= event.bend <= 8191):
        raise ValueError("Invalid pitch bend: bend must be in -8192..8191")
    if destinations is not None and event.channel not in set(destinations):
        raise ValueError(f"Invalid route: no destination for channel={event.channel}")


def ticks_to_beats(ticks: int, ppq: int) -> float:
    if ticks < 0 or ppq <= 0:
        raise ValueError("ticks must be nonnegative and PPQ positive")
    return ticks / ppq


def beats_to_seconds(beats: float, bpm: float) -> float:
    if beats < 0 or bpm <= 0:
        raise ValueError("beats must be nonnegative and BPM positive")
    return beats * 60.0 / bpm


def seconds_to_samples(seconds: float, sample_rate: int) -> int:
    if seconds < 0 or sample_rate <= 0:
        raise ValueError("seconds must be nonnegative and sample rate positive")
    return round(seconds * sample_rate)


def tick_to_seconds(tick: int, tempos: list[TempoEvent], ppq: int = 480) -> float:
    """Integrate a piecewise-constant tempo map up to ``tick``."""
    if tick < 0 or ppq <= 0 or not tempos:
        raise ValueError("tick/PPQ must be valid and a tempo map is required")
    ordered = sorted(tempos, key=lambda x: x.tick)
    if ordered[0].tick != 0 or any(t.bpm <= 0 or t.tick < 0 for t in ordered):
        raise ValueError("tempo map must begin at tick 0 and contain valid tempos")
    seconds, previous_tick, bpm = 0.0, 0, ordered[0].bpm
    for change in ordered[1:]:
        if change.tick > tick:
            break
        seconds += beats_to_seconds((change.tick - previous_tick) / ppq, bpm)
        previous_tick, bpm = change.tick, change.bpm
    return seconds + beats_to_seconds((tick - previous_tick) / ppq, bpm)


def schedule(events: Iterable[MidiEvent], tempos: list[TempoEvent], ppq: int = 480,
             destinations: Iterable[int] | None = None) -> list[ScheduledEvent]:
    checked = list(events)
    for event in checked:
        validate_event(event, destinations)
    ordered = sorted(checked, key=lambda e: (e.tick, EVENT_PRIORITY[e.type], e.track, e.order))
    return [ScheduledEvent(tick_to_seconds(e.tick, tempos, ppq), e) for e in ordered]


def quantize_tick(tick: int, grid_ticks: int, strength: float = 1.0) -> int:
    if tick < 0 or grid_ticks <= 0 or not 0 <= strength <= 1:
        raise ValueError("invalid quantization tick, grid, or strength")
    target = math.floor(tick / grid_ticks + 0.5) * grid_ticks
    return round(tick + strength * (target - tick))


def swing_tick(tick: int, subdivision_ticks: int, amount: float = 2 / 3) -> int:
    """Delay odd subdivisions; ``amount`` is their position within each pair."""
    if tick < 0 or subdivision_ticks <= 0 or not .5 <= amount < 1:
        raise ValueError("swing amount must be in [0.5, 1)")
    index, offset = divmod(tick, subdivision_ticks)
    if index % 2 == 1 and offset == 0:
        pair_start = (index - 1) * subdivision_ticks
        return round(pair_start + amount * 2 * subdivision_ticks)
    return tick


def bend_frequency(note: int, bend: int, range_semitones: float) -> float:
    midi_to_frequency(note)
    if not -8192 <= bend <= 8191 or range_semitones <= 0:
        raise ValueError("invalid bend value or configured range")
    normalized = bend / (8192 if bend < 0 else 8191)
    return midi_to_frequency(note) * 2 ** (normalized * range_semitones / 12)


class Router:
    """Explicit channel-to-patch and controller mapping for an offline synth."""
    def __init__(self, patches: Mapping[int, Patch], controls: Mapping[int, str] | None = None):
        self.patches = dict(patches)
        self.controls = dict(controls or {7: "amplitude", 74: "cutoff_hz"})

    def route(self, events: Iterable[MidiEvent], tempos: list[TempoEvent], ppq: int = 480,
              sample_rate: int = 16_000) -> list[float]:
        scheduled = schedule(events, tempos, ppq, self.patches)
        active: dict[tuple[int, int], tuple[float, int, Patch]] = {}
        voices: list[tuple[Patch, SynthNote]] = []
        patches = dict(self.patches)
        for item in scheduled:
            e = item.event
            if e.type == "control_change":
                parameter = self.controls.get(e.controller)
                if parameter is None:
                    raise ValueError(f"controller {e.controller} has no parameter mapping")
                patch = patches[e.channel]
                if parameter == "amplitude":
                    patches[e.channel] = replace(patch, amplitude=e.value / 127)
                elif parameter == "cutoff_hz":
                    patches[e.channel] = replace(patch, cutoff_hz=100 + (e.value / 127) * 3900)
                else:
                    raise ValueError(f"controller maps to nonexistent parameter={parameter!r}")
            elif e.type == "note_on" and e.velocity:
                active[(e.channel, e.note)] = (item.seconds, e.velocity, patches[e.channel])
            elif e.type == "note_off" or (e.type == "note_on" and e.velocity == 0):
                key = (e.channel, e.note)
                if key in active:
                    start, velocity, patch = active.pop(key)
                    voices.append((patch, SynthNote(e.note, start, item.seconds - start, velocity / 127)))
        if active:
            hanging = ", ".join(f"ch{c}/note{n}" for c, n in active)
            raise ValueError(f"stuck note: missing note_off for {hanging}")
        rendered = [(round(n.start * sample_rate), render_sequence(p, [replace(n, start=0)], sample_rate))
                    for p, n in voices]
        length = max((start + len(audio) for start, audio in rendered), default=0)
        output = [0.0] * length
        for start, audio in rendered:
            for i, value in enumerate(audio): output[start + i] += value
        peak = max((abs(x) for x in output), default=1)
        return [x / max(1, peak) for x in output]


def sequence_duration(events: Iterable[MidiEvent], tempos: list[TempoEvent], ppq: int = 480) -> float:
    events = list(events)
    return tick_to_seconds(max((e.tick for e in events), default=0), tempos, ppq)


# Narrow Standard MIDI File format-0 adapter. It deliberately supports only the
# chapter's note/CC/tempo subset; use a full MIDI library for general files.
def _vlq(value: int) -> bytes:
    if value < 0: raise ValueError("VLQ cannot encode negative values")
    parts = [value & 0x7f]
    value >>= 7
    while value: parts.append((value & 0x7f) | 0x80); value >>= 7
    return bytes(reversed(parts))


def write_midi_file(path: Path, events: Iterable[MidiEvent], bpm: float = 120, ppq: int = 480) -> None:
    body = bytearray(_vlq(0) + b"\xff\x51\x03" + round(60_000_000 / bpm).to_bytes(3, "big"))
    previous = 0
    for e in schedule(events, [TempoEvent(0, bpm)], ppq):
        event = e.event
        body += _vlq(event.tick - previous); previous = event.tick
        status = {"note_off": 0x80, "note_on": 0x90, "control_change": 0xB0}.get(event.type)
        if status is None: raise ValueError("SMF subset supports note and control-change events")
        first = event.note if event.note is not None else event.controller
        second = event.velocity if event.velocity is not None else event.value
        body += bytes([status | event.channel, first, second])
    body += b"\x00\xff\x2f\x00"
    path.write_bytes(b"MThd" + struct.pack(">IHHH", 6, 0, 1, ppq) + b"MTrk" + struct.pack(">I", len(body)) + body)


def read_midi_file(path: Path) -> tuple[int, list[MidiEvent]]:
    data = memoryview(path.read_bytes())
    if data[:4] != b"MThd" or data[14:18] != b"MTrk": raise ValueError("unsupported MIDI file")
    ppq, position, tick, events, order = struct.unpack(">H", data[12:14])[0], 22, 0, [], 0
    end = position + struct.unpack(">I", data[18:22])[0]
    while position < end:
        delta = 0
        while True:
            byte = data[position]; position += 1; delta = (delta << 7) | (byte & 0x7f)
            if not byte & 0x80: break
        tick += delta; status = data[position]; position += 1
        if status == 0xff:
            kind = data[position]; length = data[position + 1]; position += 2 + length
            if kind == 0x2f: break
            continue
        kind, channel = status & 0xf0, status & 0x0f
        first, second = data[position], data[position + 1]; position += 2
        name = {0x80: "note_off", 0x90: "note_on", 0xB0: "control_change"}.get(kind)
        if name is None: raise ValueError("unsupported event in educational SMF subset")
        kwargs = ({"note": first, "velocity": second} if kind != 0xB0 else
                  {"controller": first, "value": second})
        events.append(MidiEvent(tick, name, channel, order=order, **kwargs)); order += 1
    return ppq, events
