import math
from pathlib import Path
import wave

import pytest

from tech_music.music import (MAJOR, MAJOR_TRIAD, NoteEvent, arrangement_svg,
                              click_positions, midi_to_frequency,
                              note_name_to_midi, render_events,
                              seconds_per_beat, step_positions, transpose)


@pytest.mark.parametrize("bpm, expected", [(60, 1.0), (90, 2 / 3),
                                            (120, 0.5), (150, 0.4)])
def test_tempo_reference_points(bpm, expected):
    assert seconds_per_beat(bpm) == pytest.approx(expected)


def test_click_positions_start_at_downbeat_and_follow_tempo():
    assert click_positions(120, 4) == [0.0, 0.5, 1.0, 1.5]


@pytest.mark.parametrize("note, expected", [(57, 220), (69, 440), (81, 880)])
def test_midi_frequency_reference_points(note, expected):
    assert math.isclose(midi_to_frequency(note), expected, rel_tol=1e-12)


def test_note_names_scales_chords_and_swing():
    assert note_name_to_midi("C4") == 60
    assert note_name_to_midi("F#3") == 54
    assert transpose(60, MAJOR) == [60, 62, 64, 65, 67, 69, 71, 72]
    assert transpose(60, MAJOR_TRIAD) == [60, 64, 67]
    assert step_positions([1, 1, 1], 120, swing=.5) == [0, .1875, .25]


def test_validation():
    for operation in (lambda: seconds_per_beat(0), lambda: midi_to_frequency(128),
                      lambda: note_name_to_midi("H4"), lambda: NoteEvent(60, -1, 1)):
        with pytest.raises(ValueError):
            operation()


def test_render_and_visualize(tmp_path: Path):
    wav_path, svg_path = tmp_path / "notes.wav", tmp_path / "form.svg"
    render_events([NoteEvent(69, 0, .25)], wav_path)
    arrangement_svg(svg_path, [("A", 1, ("bass",)), ("B", 1, ())])
    with wave.open(str(wav_path), "rb") as audio:
        assert audio.getparams()[:3] == (1, 2, 22_050)
        assert audio.getnframes() > 0
    assert "Arrangement" in svg_path.read_text()
