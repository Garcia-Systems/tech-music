"""Small, deterministic sequencer for the Part III track.

The implementation intentionally keeps score data, arrangement data, rendering,
and visualization separate.  It is a teaching tool, not a real-time synth.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import math
import random

from .music import midi_to_frequency, seconds_per_beat
from .waveform import write_wav

SAMPLE_RATE = 22_050
BPM = 120.0
BEATS_PER_BAR = 4
STEPS_PER_BEAT = 4


@dataclass(frozen=True)
class Event:
    layer: str
    start: float
    duration: float
    pitch: int | None = None
    velocity: float = 0.7

    def __post_init__(self) -> None:
        if self.layer not in {"kick", "clap", "hat", "perc", "bass", "chords", "synth", "texture"}:
            raise ValueError(f"unknown layer: {self.layer}")
        if self.start < 0 or self.duration <= 0 or not 0 <= self.velocity <= 1:
            raise ValueError("invalid event timing or velocity")
        if self.pitch is not None and not 0 <= self.pitch <= 127:
            raise ValueError("pitch must be in the MIDI range")


@dataclass(frozen=True)
class Section:
    name: str
    bars: int
    layers: tuple[str, ...]
    variation: str = "base"

    def __post_init__(self) -> None:
        if self.bars <= 0:
            raise ValueError("a section needs at least one bar")


ARRANGEMENT = (
    Section("intro", 2, ("kick", "hat")),
    Section("groove", 2, ("kick", "clap", "hat", "perc", "bass")),
    Section("development", 2, ("kick", "clap", "hat", "perc", "bass", "chords")),
    Section("breakdown", 2, ("chords", "texture", "synth")),
    Section("build", 2, ("hat", "perc", "chords", "synth"), "build"),
    Section("main-return", 2, ("kick", "clap", "hat", "perc", "bass", "chords", "synth", "texture"), "return"),
    Section("outro", 2, ("kick", "hat", "bass")),
)


def arrangement_beats(sections: tuple[Section, ...] = ARRANGEMENT) -> float:
    return sum(section.bars for section in sections) * BEATS_PER_BAR


def arrangement_seconds(bpm: float = BPM, sections: tuple[Section, ...] = ARRANGEMENT) -> float:
    return arrangement_beats(sections) * seconds_per_beat(bpm)


def loop_events(variation: str = "base") -> list[Event]:
    """Return one four-beat house-derived loop in beat units."""
    events: list[Event] = []
    for beat in range(4):
        events.append(Event("kick", beat, .18, velocity=.78 if beat else .9))
    events += [Event("clap", beat, .12, velocity=.58) for beat in (1, 3)]
    events += [Event("hat", step / 4, .07, velocity=.28 if step % 4 else .20)
               for step in range(2, 16, 2)]
    events += [Event("perc", step / 4, .08, velocity=.24) for step in (3, 10, 15)]
    roots = (36, 36, 41, 43) if variation != "return" else (36, 36, 43, 41)
    events += [Event("bass", beat + .5, .38, pitch, .52) for beat, pitch in enumerate(roots)]
    for root in (60,):
        events += [Event("chords", 0, 3.7, root + interval, .20) for interval in (0, 3, 7)]
    motif = ((72, .5), (75, 1.5), (67, 2.5), (70, 3.25))
    if variation == "return":
        motif = ((72, .5), (75, 1.5), (79, 2.5), (82, 3.25))
    events += [Event("synth", start, .22, pitch, .25) for pitch, start in motif]
    events += [Event("texture", 0, 4, 84, .08)]
    if variation == "build":
        events += [Event("perc", 3 + step / 4, .06, velocity=.20 + step * .03) for step in range(4)]
    return events


def build_score(sections: tuple[Section, ...] = ARRANGEMENT) -> list[Event]:
    score: list[Event] = []
    cursor = 0.0
    for section in sections:
        pattern = loop_events(section.variation)
        for bar in range(section.bars):
            offset = cursor + bar * BEATS_PER_BAR
            score.extend(Event(e.layer, e.start + offset, e.duration, e.pitch, e.velocity)
                         for e in pattern if e.layer in section.layers)
        cursor += section.bars * BEATS_PER_BAR
    return score


def validate_score(events: list[Event], total_beats: float) -> None:
    for event in events:
        if event.start + event.duration > total_beats + 1e-9:
            raise ValueError(f"{event.layer} event crosses the arrangement boundary")


def _sound(event: Event, frames: int, sample_rate: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    out: list[float] = []
    frequency = midi_to_frequency(event.pitch or 60)
    for i in range(frames):
        t = i / sample_rate
        progress = i / max(1, frames - 1)
        if event.layer == "kick":
            value = math.sin(2 * math.pi * (58 - 24 * progress) * t) * math.exp(-9 * progress)
        elif event.layer in {"clap", "hat", "perc"}:
            decay = {"clap": 7, "hat": 13, "perc": 9}[event.layer]
            value = rng.uniform(-1, 1) * math.exp(-decay * progress)
        else:
            harmonic = .25 * math.sin(2 * math.pi * frequency * 2 * t)
            value = (math.sin(2 * math.pi * frequency * t) + harmonic) * math.sin(math.pi * progress)
        out.append(value * event.velocity)
    return out


def render(events: list[Event], path: Path, bpm: float = BPM,
           total_beats: float | None = None, sample_rate: int = SAMPLE_RATE) -> list[float]:
    """Render a normalized mono PCM file and return its sample data."""
    if not events:
        raise ValueError("cannot render an empty score")
    end = total_beats if total_beats is not None else max(e.start + e.duration for e in events)
    validate_score(events, end)
    beat_seconds = seconds_per_beat(bpm)
    output = [0.0] * round(end * beat_seconds * sample_rate)
    for number, event in enumerate(events):
        start = round(event.start * beat_seconds * sample_rate)
        frames = min(round(event.duration * beat_seconds * sample_rate), len(output) - start)
        for index, value in enumerate(_sound(event, frames, sample_rate, number)):
            output[start + index] += value
    peak = max(abs(value) for value in output) or 1
    gain = min(1.0, .92 / peak)
    output = [value * gain for value in output]
    path.parent.mkdir(parents=True, exist_ok=True)
    write_wav(path, output, sample_rate)
    return output


def grid_svg(events: list[Event], path: Path, beats: float = 4) -> None:
    layers = [layer for layer in ("kick", "clap", "hat", "perc", "bass", "chords", "synth", "texture")
              if any(e.layer == layer and e.start < beats for e in events)]
    width, left, top, row_h = 920, 100, 48, 32
    cells = int(beats * STEPS_PER_BEAT)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{top + row_h * len(layers) + 24}">',
             '<rect width="100%" height="100%" fill="white"/>',
             '<text x="460" y="24" text-anchor="middle" font-family="sans-serif">Events from the score data</text>']
    for row, layer in enumerate(layers):
        y = top + row * row_h
        parts.append(f'<text x="8" y="{y+21}" font-family="sans-serif">{layer}</text>')
        for cell in range(cells):
            x, w = left + cell * (800 / cells), 800 / cells
            active = any(e.layer == layer and abs(e.start - cell / STEPS_PER_BEAT) < 1e-9 for e in events)
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="27" fill="{"#e76f51" if active else "#edf2f4"}" stroke="white"/>')
    parts.append('</svg>\n')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")


def arrangement_svg(path: Path, sections: tuple[Section, ...] = ARRANGEMENT) -> None:
    layers = ("kick", "clap", "hat", "perc", "bass", "chords", "synth", "texture")
    width, left, top, row_h = 1000, 110, 52, 32
    total = sum(s.bars for s in sections)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{top + row_h * len(layers) + 25}">',
             '<rect width="100%" height="100%" fill="white"/>',
             '<text x="500" y="23" text-anchor="middle" font-family="sans-serif">Part III arrangement (width = bars)</text>']
    cursor = 0
    for section in sections:
        x, w = left + 870 * cursor / total, 870 * section.bars / total
        parts.append(f'<text x="{x+w/2:.1f}" y="43" text-anchor="middle" font-size="11">{section.name}</text>')
        for row, layer in enumerate(layers):
            y = top + row * row_h
            if cursor == 0:
                parts.append(f'<text x="8" y="{y+21}" font-family="sans-serif">{layer}</text>')
            fill = "#457b9d" if layer in section.layers else "#edf2f4"
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="27" fill="{fill}" stroke="white"/>')
        cursor += section.bars
    parts.append('</svg>\n')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the inspectable Part III track")
    parser.add_argument("--output-dir", type=Path, default=Path("assets/part-03"))
    args = parser.parse_args()
    score = build_score()
    total = arrangement_beats()
    # Each stage is reproducible from the same score; no separate hand-edited mixes.
    stages = (("01-kick", {"kick"}), ("02-drums", {"kick", "clap", "hat", "perc"}),
              ("03-drums-bass", {"kick", "clap", "hat", "perc", "bass"}),
              ("04-add-harmony", {"kick", "clap", "hat", "perc", "bass", "chords"}),
              ("05-add-synth", {"kick", "clap", "hat", "perc", "bass", "chords", "synth"}),
              ("06-add-texture", {e.layer for e in score}))
    for name, layers in stages:
        selected = [e for e in score if e.layer in layers]
        render(selected, args.output_dir / f"{name}.wav", total_beats=total)
    render(score, args.output_dir / "09-complete-track.wav", total_beats=total)
    grid_svg(loop_events(), args.output_dir / "rhythmic-grid.svg")
    arrangement_svg(args.output_dir / "arrangement.svg")
    print(f"Wrote 7 WAV files and 2 SVG files to {args.output_dir}")


if __name__ == "__main__":
    main()
