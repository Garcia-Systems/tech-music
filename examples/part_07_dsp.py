"""Generate Part VII listening files, SVG diagnostics, and rack metadata."""

from pathlib import Path
import json
import math

from tech_music.digital_audio import sine, write_pcm16
from tech_music.dsp import (DSPRack, OnePoleLowPass, compress, convolve, dft,
                            envelope, gain, hard_clip, hann, mix, peak, soft_clip)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "part-07"


def svg(name: str, title: str, series: list[tuple[str, list[float]]]) -> None:
    width, height = 800, 320
    colors = ["#2563eb", "#dc2626", "#059669", "#7c3aed"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="25" y="28" font-family="sans-serif" font-size="18">{title}</text>',
             '<line x1="30" y1="155" x2="770" y2="155" stroke="#aaa"/>']
    for number, (label, values) in enumerate(series):
        if not values:
            continue
        stride = max(1, len(values) // 700)
        view = values[::stride]
        maximum = max(max(map(abs, view)), 1e-12)
        points = " ".join(f"{30 + 740*i/max(1,len(view)-1):.1f},{155-105*v/maximum:.1f}"
                          for i, v in enumerate(view))
        parts += [f'<polyline points="{points}" fill="none" stroke="{colors[number%4]}"/>',
                  f'<text x="{35+number*185}" y="300" fill="{colors[number%4]}" font-family="sans-serif">{label}</text>']
    (OUT / name).write_text("".join(parts) + "</svg>", encoding="utf-8")


def spectrum(samples: list[float], size: int = 256) -> list[float]:
    frame = (samples[:size] + [0] * size)[:size]
    return [abs(value) for value in dft(frame)[:size // 2]]


def spectrogram_svg(name: str, samples: list[float], size: int = 128, hop: int = 64) -> None:
    """Draw a tiny dependency-free STFT magnitude heatmap."""
    windows = []
    taper = hann(size)
    for start in range(0, len(samples) - size + 1, hop):
        frame = [samples[start + n] * taper[n] for n in range(size)]
        windows.append([abs(value) for value in dft(frame)[:size // 2]])
    maximum = max(value for frame in windows for value in frame)
    cells = []
    for x, frame in enumerate(windows):
        for bin_number, value in enumerate(frame):
            shade = round(255 * math.sqrt(value / maximum)) if maximum else 0
            y = size // 2 - 1 - bin_number
            cells.append(f'<rect x="{40+x*8}" y="{35+y*4}" width="8" height="4" fill="rgb({shade},40,{255-shade})"/>')
    content = ('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="320">'
               '<rect width="100%" height="100%" fill="white"/>'
               '<text x="25" y="22" font-family="sans-serif">Chirp STFT: time →, frequency ↑</text>'
               + "".join(cells) + '</svg>')
    (OUT / name).write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rate = 16_000
    clean = sine(220, .35, rate, .55)
    rich = mix(clean, sine(440, .35, rate, .2), sine(660, .35, rate, .12))
    clipped, soft = hard_clip(gain(clean, 3), .7), soft_clip(clean, 3)
    filtered = OnePoleLowPass.from_cutoff(700, rate).process(rich)
    compressed = compress(gain(rich, 1.4), .45, 4, 5, 80, rate)
    impulse = [1] + [0] * 399 + [.45] + [0] * 799 + [.2]
    reverbed = convolve(clean, impulse)[:len(clean)]
    configs = [{"type": "gain", "value": .8}, {"type": "lowpass", "cutoff_hz": 1400},
               {"type": "distortion", "drive": 1.5},
               {"type": "delay", "milliseconds": 90, "feedback": .35, "mix": .2}]
    rack = DSPRack(configs, rate)
    rack_output = rack.process(rich)
    alternate = DSPRack([{"type": "distortion", "drive": 1.5},
                         {"type": "lowpass", "cutoff_hz": 1400}], rate).process(rich)
    sounds = {"clean": clean, "gain-clipped": clipped, "filtered": filtered,
              "soft-clipped": soft, "compressed": compressed, "reverberated": reverbed,
              "dsp-rack-output": rack_output, "alternate-chain-order": alternate}
    for name, samples in sounds.items():
        write_pcm16(OUT / f"{name}.wav", [[max(-1, min(1, x)) for x in samples]], rate)
    env = envelope(gain(rich, 1.4), 5, 80, rate)
    off_bin = sine(437, 256 / rate, rate, .8)
    windowed = [a * b for a, b in zip(off_bin, hann(256))]
    plots = {
        "gain-mixing": [("input", clean[:300]), ("gain", gain(clean, .5)[:300]), ("mix", rich[:300])],
        "phase-cancellation": [("signal", clean[:300]), ("opposite", gain(clean, -1)[:300]), ("sum", mix(clean, gain(clean, -1))[:300])],
        "delay-reverb": [("dry", clean[:1600]), ("reverb", reverbed[:1600])],
        "filter-eq": [("input spectrum", spectrum(rich)), ("low-pass spectrum", spectrum(filtered))],
        "waveshaping": [("clean", clean[:300]), ("hard", clipped[:300]), ("soft", soft[:300])],
        "compression-envelope": [("input", gain(rich, 1.4)[:1600]), ("envelope", env[:1600]), ("output", compressed[:1600])],
        "impulse-convolution": [("impulse response", impulse), ("output", reverbed[:1600])],
        "time-frequency": [("waveform", rich[:300]), ("spectrum", spectrum(rich))],
        "fourier-series": [("fundamental", clean[:300]), ("three harmonics", rich[:300])],
        "spectral-leakage": [("rectangular", spectrum(off_bin)), ("Hann", spectrum(windowed))],
        "effects-chain": [("input", rich[:500]), ("output", rack_output[:500])],
        "block-processing": [("whole/stateful", filtered[:500])],
    }
    for name, values in plots.items():
        svg(f"{name}.svg", name.replace("-", " ").title(), values)
    chirp = [0.7 * math.sin(2 * math.pi * (180 * n / rate + 1200 * (n / rate) ** 2))
             for n in range(4096)]
    spectrogram_svg("stft-spectrogram.svg", chirp)
    metadata = rack.diagnostics(rich, rack_output)
    metadata["artifacts"] = {"wav": len(sounds), "svg": len(plots) + 1}
    (OUT / "rack-diagnostics.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Generated {len(sounds)} WAV, {len(plots) + 1} SVG, and rack metadata in {OUT}")
    print(f"Rack output peak: {peak(rack_output):.6f}")


if __name__ == "__main__":
    main()
