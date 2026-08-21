"""Minimal, inspectable DAW concepts for Part IV.

This is an offline teaching renderer, not a real-time audio engine or DAW.
Session state stays as plain JSON-compatible data so references and faults are
easy to inspect.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from .waveform import write_wav

SAMPLE_RATE = 22_050


def load_session(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def duration_beats(session: dict[str, Any]) -> float:
    return max((r["start"] + r["duration"] for t in session["tracks"] for r in t["regions"]), default=0.0)


def route_path(edges: list[list[str]], source: str, destination: str) -> list[str] | None:
    """Return one breadth-first path, or None when the destination is silent."""
    queue: list[tuple[str, list[str]]] = [(source, [source])]
    seen: set[str] = set()
    while queue:
        node, path = queue.pop(0)
        if node == destination:
            return path
        if node in seen:
            continue
        seen.add(node)
        queue.extend((b, path + [b]) for a, b in edges if a == node and b not in seen)
    return None


def automation_value(points: list[dict[str, float]], beat: float) -> float:
    """Linearly interpolate sorted points, holding the end values outside them."""
    if not points:
        return 1.0
    points = sorted(points, key=lambda p: p["time"])
    if beat <= points[0]["time"]:
        return points[0]["value"]
    for left, right in zip(points, points[1:]):
        if beat <= right["time"]:
            span = right["time"] - left["time"]
            return right["value"] if span == 0 else left["value"] + (right["value"] - left["value"]) * (beat - left["time"]) / span
    return points[-1]["value"]


def validate_session(session: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    tempo = session.get("tempo", 0)
    if tempo <= 0:
        errors.append("tempo must be positive")
    tracks = session.get("tracks", [])
    ids = [t.get("id") for t in tracks]
    if len(ids) != len(set(ids)):
        errors.append("duplicate track ID")
    nodes = set(ids) | {b["id"] for b in session.get("buses", [])} | {"master", "output"}
    sources = set(session.get("sources", {}))
    for track in tracks:
        for region in track.get("regions", []):
            if region.get("start", -1) < 0 or region.get("duration", 0) <= 0:
                errors.append(f"invalid region boundary: {region.get('id')}")
            if region.get("source") not in sources:
                errors.append(f"missing source: {region.get('source')}")
    edges = session.get("routing", [])
    if len({tuple(e) for e in edges}) != len(edges):
        errors.append("duplicate route")
    for source, destination in edges:
        if source not in nodes or destination not in nodes:
            errors.append(f"route has missing endpoint: {source} -> {destination}")
    for track_id in ids:
        if route_path(edges, track_id, "output") is None:
            errors.append(f"no output path: {track_id}")
    processors = [*session.get("processors", []), *(p for b in session.get("buses", []) for p in b.get("processors", []))]
    for processor in processors:
        mix = processor.get("parameters", {}).get("mix", 0.0)
        if not 0 <= mix <= 1:
            errors.append(f"processor mix outside [0, 1]: {processor.get('id')}")
    end = duration_beats(session)
    for lane in session.get("automation", []):
        for point in lane.get("points", []):
            if not 0 <= point["value"] <= 1:
                errors.append(f"automation value outside [0, 1]: {lane.get('target')}")
            if not 0 <= point["time"] <= end:
                errors.append(f"automation time outside session: {lane.get('target')}")
    return errors


def _source(source: dict[str, Any], frames: int, sample_rate: int) -> list[float]:
    frequency = float(source.get("frequency", 220))
    return [math.sin(2 * math.pi * frequency * i / sample_rate) * float(source.get("amplitude", .2)) for i in range(frames)]


def render_session(session: dict[str, Any], path: Path, sample_rate: int = SAMPLE_RATE) -> list[float]:
    errors = validate_session(session)
    if errors:
        raise ValueError("; ".join(errors))
    seconds_per_beat = 60 / session["tempo"]
    beats = duration_beats(session)
    output = [0.0] * round(beats * seconds_per_beat * sample_rate)
    lanes = {lane["target"]: lane["points"] for lane in session.get("automation", [])}
    for track in session["tracks"]:
        if track.get("mute", False):
            continue
        gain = float(track.get("gain", 1.0))
        for region in track["regions"]:
            start = round(region["start"] * seconds_per_beat * sample_rate)
            frames = round(region["duration"] * seconds_per_beat * sample_rate)
            signal = _source(session["sources"][region["source"]], frames, sample_rate)
            for i, value in enumerate(signal[:len(output) - start]):
                beat = (start + i) / sample_rate / seconds_per_beat
                auto = automation_value(lanes.get(f"{track['id']}.gain", []), beat)
                output[start + i] += value * gain * auto
    # A tiny shared-delay demonstration stands in for the reverb bus.
    wet = next((p["parameters"]["mix"] for b in session.get("buses", []) for p in b.get("processors", []) if p["type"] == "delay"), 0.0)
    delay = round(.12 * sample_rate)
    dry = output[:]
    for i in range(delay, len(output)):
        output[i] += dry[i - delay] * wet
    peak = max((abs(v) for v in output), default=0.0)
    if peak > 1:
        raise ValueError(f"render clips: peak {peak:.3f}")
    path.parent.mkdir(parents=True, exist_ok=True)
    write_wav(path, output, sample_rate)
    return output


def timeline_svg(session: dict[str, Any], path: Path) -> None:
    beats, width, left = duration_beats(session), 1000, 120
    height = 75 + 54 * len(session["tracks"])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">', '<rect width="100%" height="100%" fill="white"/>', '<text x="500" y="24" text-anchor="middle" font-family="sans-serif">Session timeline (beats)</text>']
    for beat in range(math.ceil(beats) + 1):
        x = left + beat / beats * 840
        parts += [f'<line x1="{x:.1f}" y1="38" x2="{x:.1f}" y2="{height-12}" stroke="#d8dee9"/>', f'<text x="{x:.1f}" y="48" font-size="10">{beat}</text>']
    for row, track in enumerate(session["tracks"]):
        y = 62 + row * 54
        parts.append(f'<text x="8" y="{y+25}" font-family="sans-serif">{track["name"]}</text>')
        for region in track["regions"]:
            x, w = left + region["start"] / beats * 840, region["duration"] / beats * 840
            parts += [f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="36" rx="4" fill="#457b9d"/>', f'<text x="{x+5:.1f}" y="{y+23}" fill="white" font-size="11">{region["id"]}</text>']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts) + "</svg>\n", encoding="utf-8")


def routing_svg(session: dict[str, Any], path: Path) -> None:
    edges = session["routing"]
    lines = ["Signal graph", *[f"{a}  →  {b}" for a, b in edges]]
    height = 48 + 28 * len(lines)
    body = "".join(f'<text x="24" y="{32+i*28}" font-family="monospace" font-size="16">{line}</text>' for i, line in enumerate(lines))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="700" height="{height}"><rect width="100%" height="100%" fill="white"/>{body}</svg>\n', encoding="utf-8")


def waveform_svg(samples: list[float], session: dict[str, Any], path: Path) -> None:
    """Plot rendered waveform and automation from the render's own data."""
    width, height, mid = 1000, 360, 115
    stride = max(1, len(samples) // 900)
    points = " ".join(f"{50+i/(len(samples)-1)*900:.1f},{mid-v*80:.1f}" for i, v in enumerate(samples) if i % stride == 0)
    lanes = session.get("automation", [])
    automation = lanes[0]["points"] if lanes else []
    end = duration_beats(session) or 1
    auto_points = " ".join(f"{50+p['time']/end*900:.1f},{315-p['value']*100:.1f}" for p in automation)
    body = (f'<text x="500" y="24" text-anchor="middle" font-family="sans-serif">Rendered waveform and gain automation</text>'
            f'<line x1="50" y1="{mid}" x2="950" y2="{mid}" stroke="#999"/><polyline points="{points}" fill="none" stroke="#457b9d"/>'
            f'<text x="50" y="190" font-family="sans-serif">automation value</text><polyline points="{auto_points}" fill="none" stroke="#e76f51" stroke-width="3"/>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="100%" height="100%" fill="white"/>{body}</svg>\n', encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate, inspect, and render the Part IV educational session")
    parser.add_argument("session", type=Path, nargs="?", default=Path("data/part-04-session.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("assets/part-04"))
    args = parser.parse_args()
    session = load_session(args.session)
    errors = validate_session(session)
    if errors:
        raise SystemExit("Session invalid:\n- " + "\n- ".join(errors))
    timeline_svg(session, args.output_dir / "timeline.svg")
    routing_svg(session, args.output_dir / "routing.svg")
    samples = render_session(session, args.output_dir / "session-render.wav")
    waveform_svg(samples, session, args.output_dir / "waveform-automation.svg")
    print(f"Valid session: {len(session['tracks'])} tracks, {duration_beats(session):g} beats, {len(samples)} samples")


if __name__ == "__main__":
    main()
