"""The small, deterministic offline music application built in Part X.

This is teaching code: mono float buffers, explicit units, JSON data, and no
real-time or third-party dependency.  Existing Part V, VII, and IX components
do the synthesis, DSP, and graph ordering work.
"""
from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
import math
from pathlib import Path
import time
from typing import Any, Iterable, Protocol

from .dsp import DSPRack, gain, peak, rms
from .engine import RoutingGraph
from .synth import ADSR, Patch, SynthNote, render_note
from .waveform import write_wav

SCHEMA_VERSION = 1
KNOWN_WAVEFORMS = {"sine", "square", "saw", "triangle"}
KNOWN_PROCESSORS = {"gain", "lowpass", "distortion", "delay"}


class Processor(Protocol):
    """The deliberately small interoperable DSP contract."""
    def process(self, samples: Iterable[float]) -> list[float]: ...


@dataclass(frozen=True)
class Tempo:
    bpm: float
    beats_per_bar: int = 4
    ticks_per_beat: int = 480

    def __post_init__(self) -> None:
        if not math.isfinite(self.bpm) or self.bpm <= 0:
            raise ValueError("tempo.bpm must be finite and greater than zero")
        if self.beats_per_bar <= 0 or self.ticks_per_beat <= 0:
            raise ValueError("tempo meter and ticks_per_beat must be positive")

    def beats_to_seconds(self, beats: float) -> float:
        return beats * 60.0 / self.bpm

    def beats_to_sample_offset(self, beats: float, sample_rate_hz: int) -> int:
        if beats < 0 or sample_rate_hz <= 0:
            raise ValueError("beats must be non-negative and sample_rate_hz positive")
        return round(self.beats_to_seconds(beats) * sample_rate_hz)

    def ticks_to_beats(self, ticks: int) -> float:
        return ticks / self.ticks_per_beat

    def bar_to_beats(self, bar: int) -> float:
        if bar < 1:
            raise ValueError("bar numbers begin at 1")
        return (bar - 1) * self.beats_per_bar


def schedule_steps(patterns: dict[str, list[int]], bpm: float,
                   steps_per_beat: int = 4, loops: int = 1) -> list[dict[str, Any]]:
    """Turn grids into data events; instruments remain a separate concern."""
    if steps_per_beat <= 0 or loops <= 0 or not patterns:
        raise ValueError("patterns, positive steps_per_beat, and positive loops required")
    lengths = {len(pattern) for pattern in patterns.values()}
    if len(lengths) != 1 or 0 in lengths:
        raise ValueError("all patterns must have the same non-zero length")
    events = []
    pattern_length = lengths.pop()
    for loop in range(loops):
        for instrument, pattern in patterns.items():
            for step_index, enabled in enumerate(pattern):
                if enabled:
                    events.append({"kind": "trigger", "instrument": instrument,
                                   "beat": (loop * pattern_length + step_index) / steps_per_beat})
    return sorted(events, key=lambda event: (event["beat"], event["instrument"]))


def automation_value(points: list[dict[str, float]], beat: float) -> float:
    """Piecewise-linear automation, with endpoint values held outside its span."""
    if not points:
        raise ValueError("automation requires at least one point")
    ordered = sorted(points, key=lambda point: point["beat"])
    if any(left["beat"] == right["beat"] for left, right in zip(ordered, ordered[1:])):
        raise ValueError("automation point beats must be unique")
    if beat <= ordered[0]["beat"]:
        return ordered[0]["value"]
    for left, right in zip(ordered, ordered[1:]):
        if beat <= right["beat"]:
            span = right["beat"] - left["beat"]
            if span <= 0:
                raise ValueError("automation point beats must be unique")
            amount = (beat - left["beat"]) / span
            return left["value"] + amount * (right["value"] - left["value"])
    return ordered[-1]["value"]


def _patch(raw: dict[str, Any]) -> Patch:
    return Patch(raw["waveform"], raw.get("amplitude", 0.5),
                 ADSR(**raw.get("envelope", {})), raw.get("cutoff_hz", 3000.0))


def load_project(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}: invalid JSON at line {error.lineno}, column {error.colno}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{path}: project root must be an object")
    return value


def save_project(project: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(project, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_project(project: dict[str, Any]) -> list[str]:
    """Return all actionable errors; never silently repair project data."""
    errors: list[str] = []
    if project.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}; got {project.get('schema_version')!r}")
    try:
        tempo = Tempo(float(project.get("tempo_bpm", 0)))
    except (TypeError, ValueError) as error:
        errors.append(str(error)); tempo = None
    sample_rate_hz = project.get("sample_rate_hz", 0)
    if not isinstance(sample_rate_hz, int) or sample_rate_hz <= 0:
        errors.append("sample_rate_hz must be a positive integer")
    duration_beats = project.get("duration_beats", 0)
    if not isinstance(duration_beats, (int, float)) or duration_beats <= 0:
        errors.append("duration_beats must be greater than zero")
    patches = project.get("patches", {})
    if not isinstance(patches, dict): errors.append("patches must be an object"); patches = {}
    for patch_id, raw in patches.items():
        try: _patch(raw).validate()
        except (KeyError, TypeError, ValueError) as error: errors.append(f'Patch "{patch_id}": {error}')
    buses = project.get("buses", [])
    bus_ids = [bus.get("id") for bus in buses if isinstance(bus, dict)]
    if "master" not in bus_ids: errors.append('A bus with id "master" is required')
    tracks = project.get("tracks", [])
    track_ids = [track.get("id") for track in tracks if isinstance(track, dict)]
    all_ids = track_ids + bus_ids
    duplicates = sorted({item for item in all_ids if item is not None and all_ids.count(item) > 1})
    if duplicates: errors.append(f"IDs must be unique; duplicates: {', '.join(duplicates)}")
    for track in tracks:
        track_id = track.get("id", "<missing>")
        if not track.get("id"): errors.append("Track is missing a non-empty id")
        if track.get("patch") not in patches: errors.append(f'Track "{track_id}" uses unknown patch "{track.get("patch")}"')
        if not 0 <= track.get("gain", 1.0) <= 2: errors.append(f'Track "{track_id}" gain must be in [0, 2]')
        for index, event in enumerate(track.get("events", [])):
            label = f'Track "{track_id}" event {index}'
            if event.get("start_unit", "beats") != "beats": errors.append(f'{label} start_unit must be "beats", not {event.get("start_unit")!r}')
            if not isinstance(event.get("note"), int) or not 0 <= event.get("note", -1) <= 127: errors.append(f"{label} note must be an integer in [0, 127]")
            if event.get("start_beat", -1) < 0 or event.get("duration_beats", 0) <= 0: errors.append(f"{label} needs non-negative start_beat and positive duration_beats")
            if event.get("start_beat", 0) + event.get("duration_beats", 0) > duration_beats: errors.append(f"{label} extends beyond duration_beats")
            if not 0 <= event.get("velocity", 1) <= 1: errors.append(f"{label} velocity must be in [0, 1]")
        for processor in track.get("processors", []):
            if processor.get("type") not in KNOWN_PROCESSORS: errors.append(f'Track "{track_id}" has unknown processor "{processor.get("type")}"')
        try:
            DSPRack(track.get("processors", []), sample_rate_hz)
        except (TypeError, ValueError) as error:
            errors.append(f'Track "{track_id}" processor: {error}')
        for lane in track.get("automation", []):
            if lane.get("parameter") != "gain": errors.append(f'Track "{track_id}" has unsupported automation parameter "{lane.get("parameter")}"')
            for point in lane.get("points", []):
                if not 0 <= point.get("value", -1) <= 2: errors.append(f'Track "{track_id}" gain automation value must be in [0, 2]')
    edges = []
    for bus in buses:
        try:
            DSPRack(bus.get("processors", []), sample_rate_hz)
        except (TypeError, ValueError) as error:
            errors.append(f'Bus "{bus.get("id", "<missing>")}" processor: {error}')
    for route in project.get("routes", []):
        source, destination = route.get("source"), route.get("destination")
        if source not in all_ids: errors.append(f'Route source "{source}" does not exist')
        if destination not in bus_ids: errors.append(f'Route destination "{destination}" is not a bus')
        if source == "master": errors.append("The master bus cannot have an outgoing route")
        edges.append((source, destination))
    destinations = {source for source, _ in edges}
    for track_id in track_ids:
        if track_id not in destinations: errors.append(f'Track "{track_id}" is disconnected: add a route to a bus')
    if all(source in all_ids and destination in all_ids for source, destination in edges):
        try: RoutingGraph(all_ids, edges).processing_order()
        except ValueError as error: errors.append(f"Routing graph: {error}")
    return errors


def _fit(samples: list[float], frame_count: int) -> list[float]:
    return (samples + [0.0] * frame_count)[:frame_count]


def render_project(project: dict[str, Any], block_size: int = 128) -> tuple[list[float], dict[str, Any]]:
    errors = validate_project(project)
    if errors: raise ValueError("project validation failed:\n- " + "\n- ".join(errors))
    started = time.perf_counter(); tempo = Tempo(float(project["tempo_bpm"]))
    sample_rate_hz = project["sample_rate_hz"]
    frame_count = tempo.beats_to_sample_offset(project["duration_beats"], sample_rate_hz)
    buffers: dict[str, list[float]] = {item["id"]: [0.0] * frame_count for item in project["tracks"] + project["buses"]}
    track_reports = []
    for track in project["tracks"]:
        patch = _patch(project["patches"][track["patch"]]); track_audio = [0.0] * frame_count
        for event in sorted(track["events"], key=lambda item: item["start_beat"]):
            start = tempo.beats_to_sample_offset(event["start_beat"], sample_rate_hz)
            note = SynthNote(event["note"], 0, tempo.beats_to_seconds(event["duration_beats"]), event.get("velocity", 1.0))
            voice = render_note(note, patch, sample_rate_hz)
            for offset, sample in enumerate(voice[:frame_count-start]): track_audio[start + offset] += sample
        for lane in track.get("automation", []):
            points = lane["points"]
            track_audio = [sample * automation_value(points, frame / sample_rate_hz * tempo.bpm / 60)
                           for frame, sample in enumerate(track_audio)]
        rack = DSPRack(track.get("processors", []), sample_rate_hz)
        processed = []
        for start in range(0, frame_count, block_size):
            processed.extend(rack.process(track_audio[start:start+block_size]))
        processed = gain(processed, 0.0 if track.get("mute") else track.get("gain", 1.0))
        buffers[track["id"]] = _fit(processed, frame_count)
        track_reports.append({"id": track["id"], "events": len(track["events"]), "peak": peak(processed)})
    routes_by_source: dict[str, list[dict[str, Any]]] = {}
    for route in project["routes"]: routes_by_source.setdefault(route["source"], []).append(route)
    order = RoutingGraph(buffers, [(r["source"], r["destination"]) for r in project["routes"]]).processing_order()
    bus_configs = {bus["id"]: bus for bus in project["buses"]}
    for node in order:
        if node in bus_configs:
            buffers[node] = DSPRack(bus_configs[node].get("processors", []), sample_rate_hz).process(buffers[node])
            buffers[node] = gain(buffers[node], bus_configs[node].get("gain", 1.0))
        for route in routes_by_source.get(node, []):
            amount = route.get("gain", 1.0)
            destination = buffers[route["destination"]]
            for frame, sample in enumerate(buffers[node]): destination[frame] += sample * amount
    master = gain(buffers["master"], project.get("master_gain", 1.0))
    report = {"sample_rate_hz": sample_rate_hz, "duration_seconds": frame_count/sample_rate_hz,
              "frame_count": frame_count, "track_count": len(project["tracks"]),
              "event_count": sum(len(t["events"]) for t in project["tracks"]),
              "peak": peak(master), "rms": rms(master), "clipping": peak(master) > 1,
              "render_seconds": time.perf_counter()-started, "tracks": track_reports}
    return master, report


def diagnostic_text(project: dict[str, Any], report: dict[str, Any] | None = None) -> str:
    errors = validate_project(project)
    lines = [f"Project: {project.get('metadata', {}).get('title', '<untitled>')}",
             f"Tracks: {len(project.get('tracks', []))}",
             f"Events: {sum(len(t.get('events', [])) for t in project.get('tracks', []))}",
             "Routes: " + ", ".join(f"{r.get('source')} -> {r.get('destination')}" for r in project.get("routes", [])),
             f"Validation: {'FAILED' if errors else 'OK'}"]
    lines.extend(f"ERROR: {error}" for error in errors)
    if report: lines += [f"Duration: {report['duration_seconds']:.3f} s", f"Peak: {report['peak']:.6f}",
                         f"RMS: {report['rms']:.6f}", f"Clipping: {report['clipping']}",
                         f"Render time: {report['render_seconds']:.6f} s"]
    return "\n".join(lines) + "\n"


def _svg(path: Path, body: str, width: int = 900, height: int = 360) -> None:
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#101522"/><style>text{{fill:#e8eefc;font:14px monospace}} .a{{fill:#56cfe1}} .b{{stroke:#ffca3a;fill:none;stroke-width:2}}</style>{body}</svg>\n', encoding="utf-8")


def plot_project(project: dict[str, Any], audio: list[float], output_directory: Path) -> list[Path]:
    output_directory.mkdir(parents=True, exist_ok=True); duration = project["duration_beats"]
    paths = [output_directory/name for name in ("arrangement.svg", "piano-roll.svg", "waveform.svg", "routing.svg")]
    rows=[]; notes=[]
    for row, track in enumerate(project["tracks"]):
        y=45+row*55; rows.append(f'<text x="10" y="{y}">{track["id"]}</text>')
        for event in track["events"]:
            x=130+700*event["start_beat"]/duration; w=max(2,700*event["duration_beats"]/duration)
            rows.append(f'<rect class="a" x="{x:.1f}" y="{y-18}" width="{w:.1f}" height="20"/>')
            notes.append(f'<rect class="a" x="{50+800*event["start_beat"]/duration:.1f}" y="{330-(event["note"]-36)*8}" width="{max(2,800*event["duration_beats"]/duration):.1f}" height="6"/>')
    _svg(paths[0], "".join(rows)); _svg(paths[1], "".join(notes))
    stride=max(1,len(audio)//1800)
    points=" ".join(f"{i*stride*899/max(1,len(audio)-1):.1f},{180-s*150:.1f}" for i,s in enumerate(audio[::stride]))
    _svg(paths[2], f'<polyline class="b" points="{points}"/>')
    ids=[t["id"] for t in project["tracks"]]+[b["id"] for b in project["buses"]]; positions={item:(80+i*800/max(1,len(ids)-1),180) for i,item in enumerate(ids)}
    graph=[]
    for route in project["routes"]:
        x1,y1=positions[route["source"]]; x2,y2=positions[route["destination"]]; graph.append(f'<line class="b" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    for item,(x,y) in positions.items(): graph.append(f'<circle class="a" cx="{x}" cy="{y}" r="28"/><text x="{x-30}" y="{y+50}">{item}</text>')
    _svg(paths[3], "".join(graph)); return paths


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(prog="tech-music", description="Part X educational offline music application")
    subs=parser.add_subparsers(dest="command", required=True)
    for name in ("validate","inspect","render","plot"):
        command=subs.add_parser(name); command.add_argument("project", type=Path)
        if name in {"render","plot"}: command.add_argument("output", type=Path)
    args=parser.parse_args(argv); project=load_project(args.project); errors=validate_project(project)
    if args.command=="validate": print("\n".join(errors) if errors else "Project is valid."); return bool(errors)
    if args.command=="inspect": print(diagnostic_text(project), end=""); return bool(errors)
    if errors: print(diagnostic_text(project), end=""); return 1
    audio,report=render_project(project)
    if args.command=="render": write_wav(args.output,audio,project["sample_rate_hz"]); print(diagnostic_text(project,report),end="")
    else: plot_project(project,audio,args.output); print(diagnostic_text(project,report),end="")
    return 0


if __name__ == "__main__": raise SystemExit(main())
