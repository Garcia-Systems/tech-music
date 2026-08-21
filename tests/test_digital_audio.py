import math
import wave

import pytest

from tech_music.digital_audio import (buffer_duration_ms, float_to_pcm16, inspect_wav,
    interleave, nyquist_frequency, pcm16_to_float, pcm_data_size, quantize,
    sample_count, sample_interval, sine, write_pcm16)


def test_time_and_rate_calculations():
    assert sample_count(2.0, 48_000) == 96_000
    assert sample_count(0.00051, 1_000) == 1  # documented nearest-frame rounding
    assert sample_interval(48_000) == pytest.approx(1 / 48_000)
    assert nyquist_frequency(48_000) == 24_000
    assert buffer_duration_ms(256, 48_000) == pytest.approx(5.333333)


def test_pcm_data_size_and_units():
    assert pcm_data_size(1, 48_000, 16, 2) == 192_000
    assert pcm_data_size(2, 8_000, 8, 1) == 16_000
    with pytest.raises(ValueError):
        pcm_data_size(1, 48_000, 12, 2)


@pytest.mark.parametrize("sample", [-1.0, -0.5, 0.0, 0.5, 1.0])
def test_pcm16_round_trip(sample):
    assert pcm16_to_float(float_to_pcm16(sample)) == pytest.approx(sample, abs=1/32767)


def test_pcm16_bounds_and_validation():
    assert float_to_pcm16(-1) == -32768
    assert float_to_pcm16(1) == 32767
    assert float_to_pcm16(2) == 32767
    with pytest.raises(ValueError):
        float_to_pcm16(2, clip=False)
    with pytest.raises(ValueError):
        float_to_pcm16(math.nan)


def test_channel_layout_and_quantization():
    assert interleave([1, 2], [10, 20]) == [1, 10, 2, 20]
    assert len(set(quantize(sine(2, 1, 32), 3))) <= 8
    with pytest.raises(ValueError):
        interleave([1], [2, 3])


def test_wav_generated_file_consistency(tmp_path):
    samples = sine(440, 0.25, 8_000, 0.8)
    path = write_pcm16(tmp_path / "test.wav", [samples, samples], 8_000)
    report = inspect_wav(path)
    assert report.sample_rate == 8_000
    assert report.channels == 2
    assert report.frames == 2_000
    assert report.sample_values == 4_000
    assert report.duration_seconds == pytest.approx(0.25)
    assert report.peak_amplitude == pytest.approx(0.8, abs=1/32767)
    assert not report.clipping
    assert report.pcm_data_bytes == 8_000
    with wave.open(str(path), "rb") as source:
        assert source.getsampwidth() == 2
