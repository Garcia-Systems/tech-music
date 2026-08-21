"""Generate, inspect, plot, and save a sine wave with Python's standard library."""
from __future__ import annotations
import argparse
from array import array
from pathlib import Path
import math
import statistics
import wave


def sine_wave(frequency: float = 440.0, duration: float = 1.0, sample_rate: int = 44_100, amplitude: float = 0.5) -> list[float]:
    """Return exactly ``round(duration * sample_rate)`` floating-point samples."""
    if frequency <= 0 or duration <= 0 or sample_rate <= 0:
        raise ValueError("frequency, duration, and sample_rate must be positive")
    if not 0 <= amplitude <= 1:
        raise ValueError("amplitude must be between 0 and 1")
    return [amplitude * math.sin(2 * math.pi * frequency * n / sample_rate)
            for n in range(round(duration * sample_rate))]


def estimate_frequency(samples: list[float], sample_rate: int) -> float:
    """Estimate a clean tone from positive-going crossings; not general pitch detection."""
    crossings = [i for i, (a, b) in enumerate(zip(samples, samples[1:])) if a <= 0 < b]
    if len(crossings) < 2:
        raise ValueError("signal needs at least two positive-going zero crossings")
    return sample_rate / statistics.fmean(b - a for a, b in zip(crossings, crossings[1:]))


def write_wav(path: Path, samples: list[float], sample_rate: int) -> None:
    """Write mono 16-bit PCM WAV, clipping safely to the representable range."""
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = array("h", (round(max(-1.0, min(1.0, value)) * 32767) for value in samples))
    if pcm.itemsize != 2:  # Defensive on unusual Python platforms.
        raise RuntimeError("16-bit signed array storage is unavailable")
    if __import__("sys").byteorder != "little": pcm.byteswap()
    with wave.open(str(path), "wb") as output:
        output.setparams((1, 2, sample_rate, len(pcm), "NONE", "not compressed"))
        output.writeframes(pcm.tobytes())


def plot_waveform(path: Path, samples: list[float], sample_rate: int, milliseconds: float = 10.0) -> None:
    """Write a dependency-free SVG plot of the opening milliseconds."""
    count = min(len(samples), round(milliseconds * sample_rate / 1000))
    width, height, pad = 800, 300, 40
    points = " ".join(
        f"{pad + i * (width - 2*pad) / max(1, count-1):.2f},{height/2 - value * (height-2*pad)/2:.2f}"
        for i, value in enumerate(samples[:count]))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/><line x1="{pad}" y1="{height/2}" x2="{width-pad}" y2="{height/2}" stroke="#aaa"/>
<polyline points="{points}" fill="none" stroke="#1769aa" stroke-width="2"/>
<text x="{width/2}" y="22" text-anchor="middle">A4 sine wave (opening 10 ms)</text>
<text x="{width/2}" y="{height-8}" text-anchor="middle">Time (ms)</text><text x="8" y="{height/2}">0</text></svg>\n'''
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(svg, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frequency", type=float, default=440.0); parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--sample-rate", type=int, default=44_100); parser.add_argument("--amplitude", type=float, default=0.5)
    parser.add_argument("--output-dir", type=Path, default=Path("assets")); args = parser.parse_args()
    samples = sine_wave(args.frequency, args.duration, args.sample_rate, args.amplitude)
    wav = args.output_dir / "audio" / "a4-sine.wav"; svg = args.output_dir / "waveforms" / "a4-sine.svg"
    write_wav(wav, samples, args.sample_rate); plot_waveform(svg, samples, args.sample_rate)
    first = "[" + " ".join(f"{v:.6f}" for v in samples[:8]) + "]"
    print(f"Generated {len(samples)} samples; first 8: {first}")
    print(f"Estimated frequency: {estimate_frequency(samples, args.sample_rate):.2f} Hz"); print(f"Wrote {wav} and {svg}")

if __name__ == "__main__": main()
