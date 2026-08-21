import json
import math

import pytest

from tech_music.music import midi_to_frequency
from tech_music.synth import (ADSR, Patch, SynthNote, VoiceManager, adsr_envelope,
                              fm_tone, load_patch, one_pole_lowpass, oscillator,
                              render_sequence)
from tech_music.waveform import estimate_frequency


def test_oscillator_count_range_frequency_and_determinism():
    first = oscillator(440, .1, 8_000, .4, .25)
    assert len(first) == 800
    assert max(map(abs, first)) <= .4 + 1e-12
    assert estimate_frequency(first, 8_000) == pytest.approx(440, abs=2)
    assert first == oscillator(440, .1, 8_000, .4, .25)


@pytest.mark.parametrize("name", ["sine", "square", "saw", "triangle"])
def test_waveforms_are_periodic(name):
    values = oscillator(100, .03, 10_000, waveform=name)
    assert values[:100] == pytest.approx(values[100:200])


def test_note_conversion_octave_and_reference():
    assert midi_to_frequency(69) == pytest.approx(440)
    assert midi_to_frequency(81) == pytest.approx(880)


def test_adsr_length_range_plateau_and_end():
    env = adsr_envelope(.5, ADSR(.1, .1, .4, .2), 100)
    assert len(env) == 70
    assert env[0] == 0
    assert env[20:50] == pytest.approx([.4] * 30)
    assert min(env) >= 0 and max(env) <= 1
    assert env[-1] == pytest.approx(0)


def test_filter_validates_and_attenuates_fast_alternation():
    with pytest.raises(ValueError, match="Nyquist"):
        one_pole_lowpass([1], 5_000, 8_000)
    source = [1, -1] * 100
    assert max(map(abs, one_pole_lowpass(source, 100, 8_000)[20:])) < .1


def test_patch_loading_and_clear_validation(tmp_path):
    data = {"version": 1, "waveform": "sine", "amplitude": .5,
            "amp_envelope": {"attack": 0, "decay": 0, "sustain": 1, "release": .1},
            "filter": {"cutoff_hz": 1000}}
    path = tmp_path / "patch.json"; path.write_text(json.dumps(data))
    assert load_patch(path).waveform == "sine"
    data.pop("filter")
    with pytest.raises(ValueError, match="missing.*filter"):
        Patch.from_dict(data)


def test_voice_allocation_note_off_and_stealing():
    voices = VoiceManager(2)
    voices.note_on(60); voices.note_on(64); voices.note_on(67)
    assert voices.active == [64, 67]
    voices.note_off(64)
    assert voices.active == [67]


def test_polyphonic_render_duration_and_clipping_limit():
    patch = Patch("saw", .8, ADSR(0, 0, 1, .2), 1500)
    audio = render_sequence(patch, [SynthNote(60, 0, .5), SynthNote(64, .25, .5)], 8_000)
    assert len(audio) == round(.95 * 8_000)
    assert max(map(abs, audio)) <= 1


def test_fm_is_deterministic_and_bounded():
    tone = fm_tone(440, 110, 40, .1, 8_000)
    assert tone == fm_tone(440, 110, 40, .1, 8_000)
    assert max(map(abs, tone)) <= .5
