import json

import pytest

from tech_music.system import (LatencyBudget, buffer_ms, deadline_margin_ms,
                               key_to_note, load_and_validate, pcm_bytes,
                               validate_workstation)


def test_pcm_storage_mono_stereo_and_multitrack():
    mono = pcm_bytes(60, 48_000, 24, 1)
    assert mono == 8_640_000
    assert pcm_bytes(60, 48_000, 24, 2) == mono * 2
    assert pcm_bytes(60, 48_000, 24, 16) == mono * 16


def test_pcm_rejects_fractional_byte_depth():
    with pytest.raises(ValueError):
        pcm_bytes(1, 48_000, 20, 2)


def test_buffer_deadline_and_latency_budget():
    assert buffer_ms(480, 48_000) == pytest.approx(10)
    assert deadline_margin_ms(480, 48_000, 7.5) == pytest.approx(2.5)
    assert LatencyBudget(1, 10, 2, 10, 1).estimated_total_ms == 24


def test_keyboard_mapping_is_deterministic():
    assert [key_to_note(k) for k in "asdfg"] == ["C4", "D4", "E4", "F4", "G4"]
    with pytest.raises(ValueError, match="unmapped"):
        key_to_note("z")


def test_working_model_and_broken_model():
    assert load_and_validate("data/part-11-workstation.json") == []
    findings = load_and_validate("data/part-11-broken-workstation.json")
    assert findings == sorted(["master is muted", "no MIDI/event route", "no audio edge reaches an output", "sample-rate mismatch"])


def test_unknown_route_is_reported_deterministically():
    config = {"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "missing", "type": "audio"}]}
    assert validate_workstation(config) == ["edge 0 references an unknown node", "no MIDI/event route"]
