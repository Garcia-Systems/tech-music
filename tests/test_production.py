from pathlib import Path
import hashlib
import math
import wave

import pytest

from tech_music.production import (ARRANGEMENT, BPM, Event, Section,
    arrangement_beats, arrangement_seconds, build_score, grid_svg, render,
    validate_score)


def test_arrangement_shape_and_duration():
    assert len(ARRANGEMENT) == 7
    assert arrangement_beats() == 56
    assert arrangement_seconds() == 28
    assert math.isclose(60 / BPM, .5)


def test_score_ranges_and_boundaries():
    score = build_score()
    validate_score(score, arrangement_beats())
    assert score
    assert all(0 <= e.start < arrangement_beats() for e in score)
    assert all(e.pitch is None or 0 <= e.pitch <= 127 for e in score)
    assert not any(e.layer == "bass" and e.start < 8 for e in score)


def test_boundary_and_data_validation():
    with pytest.raises(ValueError, match="boundary"):
        validate_score([Event("bass", 3.9, .2, 36)], 4)
    with pytest.raises(ValueError):
        Event("bass", 0, 1, 128)
    with pytest.raises(ValueError):
        Section("empty", 0, ())


def test_deterministic_render_duration_and_headroom(tmp_path: Path):
    score = build_score()
    paths = (tmp_path / "one.wav", tmp_path / "two.wav")
    samples = [render(score, path, total_beats=arrangement_beats()) for path in paths]
    assert samples[0] == samples[1]
    assert max(map(abs, samples[0])) <= .9200001
    assert hashlib.sha256(paths[0].read_bytes()).digest() == hashlib.sha256(paths[1].read_bytes()).digest()
    with wave.open(str(paths[0])) as audio:
        assert audio.getnframes() == round(arrangement_seconds() * audio.getframerate())
        assert audio.getparams()[:3] == (1, 2, 22_050)


def test_grid_comes_from_events(tmp_path: Path):
    path = tmp_path / "grid.svg"
    grid_svg([Event("kick", 0, .1)], path)
    text = path.read_text()
    assert "Events from the score data" in text and "kick" in text
