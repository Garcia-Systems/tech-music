"""Transparent music-as-data helpers used throughout Part II."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import math

from .waveform import sine_wave, write_wav

MAJOR = (0, 2, 4, 5, 7, 9, 11, 12)
NATURAL_MINOR = (0, 2, 3, 5, 7, 8, 10, 12)
MAJOR_TRIAD = (0, 4, 7)
MINOR_TRIAD = (0, 3, 7)


@dataclass(frozen=True)
class NoteEvent:
    """A note plus its position, length, and MIDI-style intensity."""

    pitch: int
    start: float
    duration: float
    velocity: int = 90

    def __post_init__(self) -> None:
        if not 0 <= self.pitch <= 127 or self.start < 0 or self.duration <= 0:
            raise ValueError("invalid pitch, start, or duration")
        if not 0 <= self.velocity <= 127:
            raise ValueError("velocity must be from 0 through 127")


def seconds_per_beat(bpm: float) -> float:
    """Convert beats per minute to seconds per beat."""
    if bpm <= 0:
        raise ValueError("bpm must be positive")
    return 60.0 / bpm


def click_positions(bpm: float, beats: int) -> list[float]:
    """Return beat timestamps starting at the downbeat (time zero)."""
    if beats < 1:
        raise ValueError("beats must be positive")
    beat = seconds_per_beat(bpm)
    return [index * beat for index in range(beats)]


def step_positions(pattern: list[int], bpm: float, steps_per_beat: int = 4,
                   swing: float = 0.0) -> list[float]:
    """Convert active grid cells to seconds; delay odd cells to add swing."""
    if steps_per_beat < 1 or not 0 <= swing < 1:
        raise ValueError("invalid subdivision or swing")
    step = seconds_per_beat(bpm) / steps_per_beat
    return [i * step + (swing * step if i % 2 else 0.0)
            for i, active in enumerate(pattern) if active]


def midi_to_frequency(note: int) -> float:
    """Convert a MIDI note number to 12-TET frequency with A4=440 Hz."""
    if not 0 <= note <= 127:
        raise ValueError("MIDI note must be from 0 through 127")
    return 440.0 * 2.0 ** ((note - 69) / 12.0)


def note_name_to_midi(name: str) -> int:
    """Convert an ASCII sharp note such as C4 or F#3 to a MIDI number."""
    pitch_classes = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
                     "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    token = name.strip().upper()
    split = 2 if len(token) >= 3 and token[1] == "#" else 1
    try:
        note = 12 * (int(token[split:]) + 1) + pitch_classes[token[:split]]
    except (KeyError, ValueError) as error:
        raise ValueError(f"invalid note name: {name}") from error
    if not 0 <= note <= 127:
        raise ValueError("note is outside the MIDI range")
    return note


def transpose(root: int, intervals: tuple[int, ...]) -> list[int]:
    """Apply semitone offsets to a root note."""
    notes = [root + interval for interval in intervals]
    if not notes or min(notes) < 0 or max(notes) > 127:
        raise ValueError("result is outside the MIDI range")
    return notes


def render_events(events: list[NoteEvent], path: Path, bpm: float = 120,
                  sample_rate: int = 22_050) -> None:
    """Render beat-based note events as a small, click-free mono sine sketch."""
    beat = seconds_per_beat(bpm)
    length = max((event.start + event.duration) * beat for event in events)
    output = [0.0] * round((length + 0.05) * sample_rate)
    for event in events:
        start = round(event.start * beat * sample_rate)
        duration = event.duration * beat
        tone = sine_wave(midi_to_frequency(event.pitch), duration, sample_rate,
                         0.18 * event.velocity / 127)
        fade = max(1, min(len(tone) // 2, round(0.008 * sample_rate)))
        for i, value in enumerate(tone):
            envelope = min(1.0, i / fade, (len(tone) - 1 - i) / fade)
            output[start + i] += value * max(0.0, envelope)
    write_wav(path, output, sample_rate)


def arrangement_svg(path: Path, sections: list[tuple[str, int, tuple[str, ...]]]) -> None:
    """Draw an accessible section/layer timeline as dependency-free SVG."""
    layers = sorted({layer for _, _, active in sections for layer in active})
    total = sum(bars for _, bars, _ in sections)
    width, left, top, cell_h = 900, 110, 55, 34
    usable = width - left - 20
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{top + cell_h * len(layers) + 40}">',
             '<rect width="100%" height="100%" fill="white"/>',
             '<text x="450" y="24" text-anchor="middle" font-family="sans-serif">Arrangement: sections and active layers</text>']
    cursor = 0
    for name, bars, active in sections:
        x, w = left + usable * cursor / total, usable * bars / total
        parts.append(f'<text x="{x + w/2:.1f}" y="44" text-anchor="middle" font-size="12">{name}</text>')
        for row, layer in enumerate(layers):
            y = top + row * cell_h
            if cursor == 0:
                parts.append(f'<text x="8" y="{y+22}" font-family="sans-serif">{layer}</text>')
            fill = "#4f86c6" if layer in active else "#eeeeee"
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="28" fill="{fill}" stroke="white"/>')
        cursor += bars
    parts.append('</svg>\n')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")


def capstone_events() -> list[NoteEvent]:
    """Return the short C-major sketch used by the capstone lab."""
    bass = [NoteEvent(p, start, 1.0, 92) for p, start in
            zip((36, 36, 41, 43, 36, 36, 43, 41), range(0, 32, 4))]
    chords = [NoteEvent(p, bar, 3.5, 56) for root, bar in
              zip((48, 53, 55, 48), range(0, 32, 8)) for p in transpose(root, MAJOR_TRIAD)]
    motif = [NoteEvent(p, start, duration, 78) for p, start, duration in
             ((60, 8, 1), (62, 9, 1), (64, 10, 2), (67, 12, 2),
              (60, 24, 1), (62, 25, 1), (65, 26, 2), (72, 28, 2))]
    return bass + chords + motif


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Part II musical sketch")
    parser.add_argument("--bpm", type=float, default=120)
    parser.add_argument("--output-dir", type=Path, default=Path("assets/part-02"))
    args = parser.parse_args()
    render_events(capstone_events(), args.output_dir / "musical-sketch.wav", args.bpm)
    arrangement_svg(args.output_dir / "arrangement.svg", [
        ("Intro", 2, ("drums",)), ("A", 2, ("drums", "bass", "chords")),
        ("Break", 2, ("chords",)), ("Return", 2, ("drums", "bass", "chords", "lead")),
    ])
    print(f"Wrote {args.output_dir / 'musical-sketch.wav'} and {args.output_dir / 'arrangement.svg'}")


if __name__ == "__main__":
    main()
