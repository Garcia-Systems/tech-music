import math

import pytest

from tech_music.dsp import (DSPRack, FeedbackDelay, OnePoleLowPass, convolve,
                            delay_samples, dft, frequency_bins, gain, hard_clip,
                            mix, peak, process_blocks)


def test_gain_mix_and_bounds():
    assert gain([.5, -.25], 2) == [1, -.5]
    assert mix([.5, -.5], [.25, .5]) == [.75, 0]
    assert peak(hard_clip([2, -3])) == 1
    with pytest.raises(ValueError):
        mix([1], [1, 2])


def test_delay_conversion_and_state_persistence():
    assert delay_samples(250, 48_000) == 12_000
    delay = FeedbackDelay(2, .5, 1)
    assert delay.process([1, 0]) == [0, 0]
    assert delay.process([0, 0, 0]) == [1, 0, .5]
    with pytest.raises(ValueError):
        FeedbackDelay(1, 1)


def test_lowpass_smooths_and_blocks_equal_whole_signal():
    source = [1, -1] * 10
    whole = OnePoleLowPass(.2).process(source)
    blocked = process_blocks(OnePoleLowPass(.2), source, 3)
    assert blocked == pytest.approx(whole)
    assert peak(whole) < peak(source)


def test_convolution_manual_example():
    expected = [1, 2.5, 1, 0]
    assert convolve([1, 2, 0], [1, .5]) == expected


def test_dft_matches_known_bins_and_frequency_mapping():
    values = [math.sin(2 * math.pi * n / 8) for n in range(8)]
    spectrum = dft(values)
    assert max(range(5), key=lambda k: abs(spectrum[k])) == 1
    assert abs(spectrum[1]) == pytest.approx(4)
    assert frequency_bins(8, 8_000)[1] == 1_000


def test_rack_validation_bypass_determinism_and_amplitude():
    config = [{"type": "gain", "value": .5},
              {"type": "lowpass", "cutoff_hz": 1_000},
              {"type": "distortion", "drive": 1.2, "bypass": True}]
    source = [.5, -.5, .25, -.25]
    first = DSPRack(config, 48_000).process(source)
    second = DSPRack(config, 48_000).process(source)
    assert first == second
    assert peak(first) <= .25
    report = DSPRack(config, 48_000).diagnostics(source, first)
    assert report["sample_rate"] == 48_000
    assert report["processors"][-1]["bypassed"] is True
    with pytest.raises(ValueError):
        DSPRack([{"type": "delay", "milliseconds": 20, "feedback": 1}], 48_000)
    with pytest.raises(ValueError):
        DSPRack([{"type": "mystery"}], 48_000)
