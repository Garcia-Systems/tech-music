import json
import wave

import pytest

from tech_music.daw import SAMPLE_RATE, automation_value, duration_beats, load_session, render_session, route_path, validate_session


@pytest.fixture
def session():
    return load_session(__import__("pathlib").Path("data/part-04-session.json"))


def test_session_references_boundaries_and_duration_are_valid(session):
    assert validate_session(session) == []
    assert duration_beats(session) == 8


def test_every_track_reaches_output(session):
    for track in session["tracks"]:
        assert route_path(session["routing"], track["id"], "output")


def test_route_path_reports_silence_and_automation_interpolates():
    assert route_path([["track", "bus"]], "track", "output") is None
    assert automation_value([{"time": 0, "value": .2}, {"time": 4, "value": .8}], 2) == pytest.approx(.5)


def test_broken_session_exposes_independent_faults():
    broken = json.loads(open("data/part-04-broken-session.json").read())
    errors = validate_session(broken)
    assert any("missing source" in error for error in errors)
    assert any("no output path: orphan" in error for error in errors)
    assert any("processor mix" in error for error in errors)
    assert any("automation time" in error for error in errors)
    assert any("automation value" in error for error in errors)


def test_render_properties(session, tmp_path):
    path = tmp_path / "render.wav"
    samples = render_session(session, path)
    assert len(samples) == 4 * SAMPLE_RATE
    assert max(abs(v) for v in samples) < 1
    with wave.open(str(path)) as wav:
        assert (wav.getframerate(), wav.getnchannels(), wav.getnframes()) == (SAMPLE_RATE, 1, len(samples))
