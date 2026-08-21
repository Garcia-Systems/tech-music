import wave
import pytest
from tech_music.waveform import estimate_frequency, plot_waveform, sine_wave, write_wav

def test_a4_sample_count_range_and_frequency():
    samples = sine_wave(440, 1, 44_100, .5)
    assert len(samples) == 44_100
    assert max(map(abs, samples)) <= .5
    assert estimate_frequency(samples, 44_100) == pytest.approx(440, abs=.2)

def test_generation_is_deterministic():
    assert sine_wave() == sine_wave()

def test_rejects_invalid_parameters():
    with pytest.raises(ValueError): sine_wave(amplitude=1.1)
    with pytest.raises(ValueError): sine_wave(frequency=0)

def test_wav_metadata(tmp_path):
    path = tmp_path / "tone.wav"; write_wav(path, sine_wave(duration=.1), 44_100)
    with wave.open(str(path), "rb") as audio:
        assert (audio.getnchannels(), audio.getsampwidth(), audio.getframerate(), audio.getnframes()) == (1, 2, 44_100, 4_410)

def test_svg_is_created(tmp_path):
    path = tmp_path / "tone.svg"; plot_waveform(path, sine_wave(duration=.02), 44_100)
    assert path.read_text().startswith('<svg xmlns="http://www.w3.org/2000/svg"')
