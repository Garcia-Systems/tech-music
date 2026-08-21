from pathlib import Path
import math

import pytest

from tech_music.midi import (MidiEvent, Router, TempoEvent, bend_frequency,
    quantize_tick, read_midi_file, schedule, seconds_to_samples, sequence_duration,
    swing_tick, tick_to_seconds, ticks_to_beats, validate_event, write_midi_file)
from tech_music.music import midi_to_frequency
from tech_music.synth import ADSR, Patch


PATCH = Patch("sine", .4, ADSR(.005, .01, .7, .02), 1500)


def pair(note=60, channel=0, start=0, end=480):
    return [MidiEvent(start, "note_on", channel, note, 90, order=0),
            MidiEvent(end, "note_off", channel, note, 0, order=1)]


@pytest.mark.parametrize("event", [
    MidiEvent(0, "note_on", note=200, velocity=1),
    MidiEvent(0, "note_on", note=60, velocity=128),
    MidiEvent(-1, "note_off", note=60, velocity=0),
    MidiEvent(0, "control_change", controller=128, value=1),
])
def test_validation_rejects_invalid_protocol_values(event):
    with pytest.raises(ValueError): validate_event(event)


def test_note_mapping_and_time_units():
    assert midi_to_frequency(69) == pytest.approx(440)
    assert midi_to_frequency(81) == pytest.approx(880)
    assert ticks_to_beats(480, 480) == 1
    assert tick_to_seconds(960, [TempoEvent(0, 120)]) == 1
    assert seconds_to_samples(.5, 48_000) == 24_000


def test_tempo_map_integrates_each_segment():
    tempos = [TempoEvent(0, 120), TempoEvent(480, 60)]
    assert tick_to_seconds(960, tempos) == pytest.approx(1.5)
    assert sequence_duration(pair(end=960), tempos) == pytest.approx(1.5)


def test_quantization_and_swing_are_explicit_transformations():
    assert quantize_tick(230, 120) == 240
    assert quantize_tick(230, 120, .5) == 235
    assert swing_tick(240, 240, 2 / 3) == 320
    assert swing_tick(0, 240, 2 / 3) == 0


def test_same_tick_order_is_deterministic_and_note_off_precedes_on():
    events = [MidiEvent(480, "note_on", note=60, velocity=90, order=2),
              MidiEvent(480, "control_change", controller=7, value=100, order=1),
              MidiEvent(480, "note_off", note=60, velocity=0, order=0)]
    first = schedule(events, [TempoEvent(0, 120)])
    second = schedule(reversed(events), [TempoEvent(0, 120)])
    assert [x.event.type for x in first] == ["control_change", "note_off", "note_on"]
    assert first == second


def test_router_lifecycle_routing_and_controller_mapping():
    events = [MidiEvent(0, "control_change", controller=7, value=80)] + pair()
    audio = Router({0: PATCH}).route(events, [TempoEvent(0, 120)], sample_rate=4000)
    assert audio and max(map(abs, audio)) > 0
    with pytest.raises(ValueError, match="destination"):
        Router({1: PATCH}).route(pair(channel=0), [TempoEvent(0, 120)])
    with pytest.raises(ValueError, match="stuck note"):
        Router({0: PATCH}).route(pair()[:1], [TempoEvent(0, 120)])
    with pytest.raises(ValueError, match="mapping"):
        Router({0: PATCH}).route([MidiEvent(0, "control_change", controller=3, value=1)], [TempoEvent(0, 120)])


def test_pitch_bend_range_is_configuration_not_a_constant():
    one_octave = bend_frequency(69, 8191, 12)
    assert one_octave == pytest.approx(880)
    assert bend_frequency(69, 8191, 2) != pytest.approx(one_octave)


def test_midi_file_subset_round_trip(tmp_path: Path):
    path = tmp_path / "phrase.mid"
    source = pair() + [MidiEvent(240, "control_change", controller=7, value=100)]
    write_midi_file(path, source, bpm=120, ppq=480)
    ppq, restored = read_midi_file(path)
    assert ppq == 480
    assert [(e.tick, e.type, e.channel, e.note, e.velocity, e.controller, e.value)
            for e in restored] == [(e.tick, e.type, e.channel, e.note, e.velocity, e.controller, e.value)
                                   for item in schedule(source, [TempoEvent(0, 120)]) for e in [item.event]]
