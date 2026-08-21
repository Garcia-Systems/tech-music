import math
import pytest

from tech_music.engine import (CommandHistory, Message, MessageQueue, MiniEngine,
    RingBuffer, RoutingGraph, Session, buffer_duration, latency_budget,
    process_file_chunks, simulate_deadlines)


def test_buffer_and_deadline_calculations():
    assert buffer_duration(256, 48_000) == pytest.approx(.005333333)
    assert latency_budget(256, 48_000, 2, .001) == pytest.approx(.011666667)
    diagnostics = simulate_deadlines([256, 256], 48_000, [.002, .006])
    assert [item.missed for item in diagnostics] == [False, True]
    assert diagnostics[0].margin_seconds == pytest.approx(.003333333)


def test_ring_buffer_empty_full_wraparound_and_order():
    ring = RingBuffer[int](2)
    with pytest.raises(BufferError): ring.read()
    ring.write(1); ring.write(2)
    with pytest.raises(BufferError): ring.write(3)
    assert ring.read() == 1
    ring.write(3)
    assert [ring.read(), ring.read()] == [2, 3]


def test_message_ordering_and_due_horizon():
    queue = MessageQueue()
    queue.put(Message(12, 1, "note_off")); queue.put(Message(4, 2, "note_on"))
    queue.put(Message(4, 1, "set_parameter"))
    assert [message.kind for message in queue.due(5)] == ["set_parameter", "note_on"]
    assert queue.due(12) == []


def test_graph_order_validation_and_cycle():
    assert RoutingGraph({"synth", "eq", "master"}, [("synth", "eq"), ("eq", "master")]).processing_order() == ["synth", "eq", "master"]
    with pytest.raises(ValueError, match="unknown"): RoutingGraph({"a"}, [("a", "missing")]).processing_order()
    with pytest.raises(ValueError, match="cycle"): RoutingGraph({"a", "b"}, [("a", "b"), ("b", "a")]).processing_order()


def test_session_round_trip_and_validation():
    session = Session(duration_frames=300, events=[Message(12, 0, "note_on", {"note": 69})])
    assert Session.from_json(session.to_json()) == session
    with pytest.raises(ValueError, match="unsupported"): Session.from_json('{"schema_version": 99}')
    assert Session(sample_rate=0).validate()


def test_sample_accurate_render_is_deterministic_and_differs_from_snapping():
    events = [Message(3, 0, "note_on", {"note": 69}), Message(11, 1, "note_off", {"note": 69})]
    session = Session(sample_rate=8000, block_size=8, duration_frames=16, events=events)
    accurate = MiniEngine(session).render()
    assert accurate == MiniEngine(Session.from_json(session.to_json())).render()
    snapped = MiniEngine(Session.from_json(session.to_json())).render(snap_events=True)
    assert accurate != snapped
    assert accurate[:3] == [0.0] * 3 and any(abs(x) > 0 for x in accurate[4:11])


def test_phase_state_persists_across_blocks():
    event = Message(0, 0, "note_on", {"note": 69})
    a = MiniEngine(Session(sample_rate=8000, block_size=7, duration_frames=31, events=[event])).render()
    b = MiniEngine(Session(sample_rate=8000, block_size=31, duration_frames=31, events=[event])).render()
    assert a == pytest.approx(b)


def test_undo_redo_and_new_edit_clears_redo():
    values = []; history = CommandHistory()
    history.execute(lambda: values.append(1), lambda: values.pop())
    history.undo(); assert values == []
    history.redo(); assert values == [1]
    history.undo(); history.execute(lambda: values.append(2), lambda: values.pop())
    with pytest.raises(IndexError): history.redo()


def test_chunked_file_processing(tmp_path):
    path = tmp_path / "audio.raw"; path.write_bytes(bytes(range(100)))
    assert process_file_chunks(path, 16) == (100, 7)
