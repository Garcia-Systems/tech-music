"""Deterministic educational models for a music-technology workstation.

These functions model configuration; they do not probe or certify real hardware.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def pcm_bytes(duration_s: float, sample_rate: int, bit_depth: int, channels: int) -> int:
    """Return payload bytes for interleaved integer PCM (excluding container overhead)."""
    if duration_s < 0 or sample_rate <= 0 or bit_depth <= 0 or channels <= 0:
        raise ValueError("duration must be non-negative; other values must be positive")
    if bit_depth % 8:
        raise ValueError("bit depth must be a whole number of bytes")
    return round(duration_s * sample_rate) * (bit_depth // 8) * channels


def buffer_ms(frames: int, sample_rate: int) -> float:
    if frames <= 0 or sample_rate <= 0:
        raise ValueError("frames and sample rate must be positive")
    return frames / sample_rate * 1000.0


def deadline_margin_ms(frames: int, sample_rate: int, processing_ms: float) -> float:
    """Positive means the simulated processing finished before its block deadline."""
    if processing_ms < 0:
        raise ValueError("processing time must be non-negative")
    return buffer_ms(frames, sample_rate) - processing_ms


@dataclass(frozen=True)
class LatencyBudget:
    input_ms: float
    input_buffer_ms: float
    processing_ms: float
    output_buffer_ms: float
    output_ms: float

    @property
    def estimated_total_ms(self) -> float:
        values = (self.input_ms, self.input_buffer_ms, self.processing_ms,
                  self.output_buffer_ms, self.output_ms)
        if any(value < 0 for value in values):
            raise ValueError("latency contributions cannot be negative")
        return sum(values)


def key_to_note(key: str, octave: int = 4) -> str:
    mapping = {"a": "C", "s": "D", "d": "E", "f": "F", "g": "G", "h": "A", "j": "B"}
    try:
        return f"{mapping[key.lower()]}{octave}"
    except KeyError as exc:
        raise ValueError(f"unmapped key: {key}") from exc


def validate_workstation(config: dict[str, Any]) -> list[str]:
    """Return stable, human-readable structural/configuration findings."""
    findings: list[str] = []
    nodes = config.get("nodes", [])
    node_ids = [node.get("id") for node in nodes]
    if len(node_ids) != len(set(node_ids)):
        findings.append("duplicate node id")
    known = set(node_ids)
    edges = config.get("edges", [])
    for index, edge in enumerate(edges):
        if edge.get("from") not in known or edge.get("to") not in known:
            findings.append(f"edge {index} references an unknown node")
    audio_edges = [(e.get("from"), e.get("to")) for e in edges if e.get("type") == "audio"]
    event_edges = [(e.get("from"), e.get("to")) for e in edges if e.get("type") in {"midi", "event"}]
    if not event_edges:
        findings.append("no MIDI/event route")
    if not audio_edges:
        findings.append("no audio route")
    output_ids = {n.get("id") for n in nodes if n.get("role") in {"speaker", "headphones", "file"}}
    if output_ids and not any(dst in output_ids for _, dst in audio_edges):
        findings.append("no audio edge reaches an output")
    rates = {n.get("sample_rate") for n in nodes if n.get("sample_rate") is not None}
    if len(rates) > 1:
        findings.append("sample-rate mismatch")
    if config.get("master_muted"):
        findings.append("master is muted")
    gain = config.get("input_gain_db")
    if gain is not None and gain > 60:
        findings.append("input gain exceeds this model's educational limit")
    frames, rate = config.get("buffer_frames"), config.get("sample_rate")
    if frames and rate and buffer_ms(frames, rate) > 25:
        findings.append("buffer contribution exceeds 25 ms")
    return sorted(findings)


def load_and_validate(path: str | Path) -> list[str]:
    return validate_workstation(json.loads(Path(path).read_text(encoding="utf-8")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Model a music workstation; no hardware is probed")
    sub = parser.add_subparsers(dest="command", required=True)
    storage = sub.add_parser("storage", help="calculate raw PCM payload size")
    storage.add_argument("--seconds", type=float, required=True)
    storage.add_argument("--rate", type=int, default=48000)
    storage.add_argument("--bits", type=int, default=24)
    storage.add_argument("--channels", type=int, default=2)
    validate = sub.add_parser("validate", help="validate a structured workstation")
    validate.add_argument("path")
    args = parser.parse_args(argv)
    if args.command == "storage":
        print(json.dumps({"pcm_payload_bytes": pcm_bytes(args.seconds, args.rate, args.bits, args.channels)}))
        return 0
    findings = load_and_validate(args.path)
    print(json.dumps({"model_only": True, "findings": findings}, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
