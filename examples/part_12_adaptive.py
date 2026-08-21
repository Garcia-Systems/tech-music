"""Render the transparent Part XII capstone into ignored ``generated/`` paths."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tech_music.generative import AdaptiveConfig, encode_events, generate, render
from tech_music.waveform import write_wav


def piano_roll(events, path: Path, duration: float) -> None:
    width, height = 800, 240
    notes = [e.note for e in events] or [60]
    low, high = min(notes) - 1, max(notes) + 1
    rects = []
    for event in events:
        x, w = event.start / duration * width, max(1, event.duration / duration * width)
        y = height - (event.note - low + 1) / (high - low + 2) * height
        rects.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="12"/>')
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="240" '
                    'viewBox="0 0 800 240"><g fill="#6b5cff">' + ''.join(rects) +
                    '</g></svg>\n', encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", default="focus")
    parser.add_argument("--seed", type=int, default=12)
    parser.add_argument("--duration", type=float, default=8)
    parser.add_argument("--output", type=Path, default=Path("generated"))
    args = parser.parse_args()
    generation = generate(AdaptiveConfig(mode=args.mode, seed=args.seed, duration=args.duration))
    for folder in ("audio", "plots", "reports"):
        (args.output / folder).mkdir(parents=True, exist_ok=True)
    write_wav(args.output / "audio" / "part-12-adaptive.wav", render(generation), 8000)
    piano_roll(generation.events, args.output / "plots" / "part-12-piano-roll.svg", args.duration)
    report = {"config": json.loads(generation.config.to_json()), "tempo": generation.tempo,
              "patch": generation.patch, "sections": generation.sections,
              "tokens": encode_events(generation.events), "decisions": generation.decisions}
    (args.output / "reports" / "part-12-generation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(generation.events)} events at {generation.tempo} BPM")


if __name__ == "__main__":
    main()
