"""Deterministic teaching models for Part IX (not a real-time audio engine)."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import heapq
import json
import math
from pathlib import Path
from typing import Any, Callable, Generic, Iterable, TypeVar


def buffer_duration(frames: int, sample_rate: int) -> float:
    if frames <= 0 or sample_rate <= 0:
        raise ValueError("frames and sample_rate must be positive")
    return frames / sample_rate


def latency_budget(frames: int, sample_rate: int, buffers: int = 2,
                   other_seconds: float = 0.0) -> float:
    if buffers < 0 or other_seconds < 0:
        raise ValueError("latency contributions cannot be negative")
    return buffers * buffer_duration(frames, sample_rate) + other_seconds


@dataclass(frozen=True, order=True)
class Message:
    sample: int
    order: int
    kind: str = field(compare=False)
    payload: dict[str, Any] = field(default_factory=dict, compare=False)


class MessageQueue:
    """Stable timestamp/sequence queue owned by its consumer."""
    def __init__(self) -> None:
        self._items: list[Message] = []

    def put(self, message: Message) -> None:
        if message.sample < 0:
            raise ValueError("message sample cannot be negative")
        heapq.heappush(self._items, message)

    def due(self, end_sample: int) -> list[Message]:
        result = []
        while self._items and self._items[0].sample < end_sample:
            result.append(heapq.heappop(self._items))
        return result


T = TypeVar("T")


class RingBuffer(Generic[T]):
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._data: list[T | None] = [None] * capacity
        self._read = self._write = self._size = 0

    def __len__(self) -> int: return self._size
    @property
    def capacity(self) -> int: return len(self._data)

    def write(self, value: T) -> None:
        if self._size == self.capacity: raise BufferError("ring buffer is full")
        self._data[self._write] = value
        self._write = (self._write + 1) % self.capacity
        self._size += 1

    def read(self) -> T:
        if not self._size: raise BufferError("ring buffer is empty")
        value = self._data[self._read]
        self._data[self._read] = None
        self._read = (self._read + 1) % self.capacity
        self._size -= 1
        return value  # type: ignore[return-value]


class RoutingGraph:
    def __init__(self, nodes: Iterable[str], edges: Iterable[tuple[str, str]]):
        self.nodes = set(nodes); self.edges = list(edges)

    def processing_order(self) -> list[str]:
        incoming = {n: 0 for n in self.nodes}; outgoing = {n: [] for n in self.nodes}
        for source, target in self.edges:
            if source not in self.nodes or target not in self.nodes:
                raise ValueError(f"unknown route endpoint: {source}->{target}")
            incoming[target] += 1; outgoing[source].append(target)
        ready = [n for n, count in incoming.items() if count == 0]; heapq.heapify(ready)
        order = []
        while ready:
            node = heapq.heappop(ready); order.append(node)
            for target in sorted(outgoing[node]):
                incoming[target] -= 1
                if incoming[target] == 0: heapq.heappush(ready, target)
        if len(order) != len(self.nodes): raise ValueError("cycle requires an explicit delayed feedback model")
        return order


@dataclass
class Session:
    sample_rate: int = 8000
    block_size: int = 128
    duration_frames: int = 8000
    events: list[Message] = field(default_factory=list)
    gain: float = 0.25
    schema_version: int = 1

    def validate(self) -> list[str]:
        errors = []
        if self.sample_rate <= 0: errors.append("sample_rate must be positive")
        if self.block_size <= 0: errors.append("block_size must be positive")
        if self.duration_frames < 0: errors.append("duration_frames cannot be negative")
        if not 0 <= self.gain <= 1: errors.append("gain must be between 0 and 1")
        if any(e.sample >= self.duration_frames for e in self.events): errors.append("event outside session")
        return errors

    def to_json(self) -> str: return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "Session":
        raw = json.loads(text)
        if raw.get("schema_version", 1) != 1: raise ValueError("unsupported session schema")
        raw["events"] = [Message(**event) for event in raw.get("events", [])]
        result = cls(**raw)
        if errors := result.validate(): raise ValueError("; ".join(errors))
        return result


@dataclass(frozen=True)
class BlockDiagnostic:
    index: int; frames: int; buffer_seconds: float; processing_seconds: float
    margin_seconds: float; missed: bool


def simulate_deadlines(frame_counts: Iterable[int], sample_rate: int,
                       processing_seconds: Iterable[float]) -> list[BlockDiagnostic]:
    result = []
    for index, (frames, elapsed) in enumerate(zip(frame_counts, processing_seconds)):
        deadline = buffer_duration(frames, sample_rate)
        result.append(BlockDiagnostic(index, frames, deadline, elapsed, deadline-elapsed, elapsed > deadline))
    return result


class MiniEngine:
    """Sample-accurate monophonic sine render with persistent phase."""
    def __init__(self, session: Session):
        if errors := session.validate(): raise ValueError("; ".join(errors))
        self.session = session

    def render(self, snap_events: bool = False) -> list[float]:
        s = self.session; output = [0.0] * s.duration_frames
        events = sorted(s.events); event_index = 0; active: dict[int, float] = {}; phase = 0.0
        gain = s.gain
        for start in range(0, s.duration_frames, s.block_size):
            end = min(start + s.block_size, s.duration_frames)
            for frame in range(start, end):
                while event_index < len(events) and ((events[event_index].sample <= frame) if not snap_events else
                      (events[event_index].sample < end and frame == start)):
                    event = events[event_index]; note = int(event.payload.get("note", 69))
                    if event.kind == "note_on": active[note] = float(event.payload.get("velocity", 1.0))
                    elif event.kind == "note_off": active.pop(note, None)
                    elif event.kind == "set_parameter" and event.payload.get("name") == "gain": gain = float(event.payload["value"])
                    event_index += 1
                if active:
                    note, velocity = next(reversed(active.items()))
                    output[frame] = math.sin(phase) * gain * velocity
                    phase = (phase + 2*math.pi*440*2**((note-69)/12)/s.sample_rate) % (2*math.pi)
        return output


class CommandHistory:
    def __init__(self): self.undo_stack: list[tuple[Callable, Callable]] = []; self.redo_stack = []
    def execute(self, do: Callable[[], None], undo: Callable[[], None]) -> None:
        do(); self.undo_stack.append((do, undo)); self.redo_stack.clear()
    def undo(self) -> None:
        if not self.undo_stack: raise IndexError("nothing to undo")
        command = self.undo_stack.pop(); command[1](); self.redo_stack.append(command)
    def redo(self) -> None:
        if not self.redo_stack: raise IndexError("nothing to redo")
        command = self.redo_stack.pop(); command[0](); self.undo_stack.append(command)


def process_file_chunks(path: Path, chunk_size: int) -> tuple[int, int]:
    if chunk_size <= 0: raise ValueError("chunk_size must be positive")
    total = chunks = 0
    with path.open("rb") as stream:
        while data := stream.read(chunk_size): total += len(data); chunks += 1
    return total, chunks
