"""Generate Part VI's short listening examples and inspectable SVG figures."""

from pathlib import Path
import math

from tech_music.digital_audio import inspect_wav, quantize, sine, write_pcm16

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "part-06"


def svg(name: str, title: str, series: list[tuple[str, list[float]]]) -> None:
    width, height = 760, 300
    colors = ["#2563eb", "#dc2626", "#059669", "#7c3aed"]
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/>',
            f'<text x="30" y="28" font-family="sans-serif" font-size="18">{title}</text>',
            '<line x1="30" y1="150" x2="730" y2="150" stroke="#999"/>']
    for index, (label, values) in enumerate(series):
        if not values:
            continue
        points = " ".join(f"{30 + 700*i/max(1, len(values)-1):.1f},{150 - 100*v:.1f}"
                          for i, v in enumerate(values))
        body.append(f'<polyline points="{points}" fill="none" stroke="{colors[index % 4]}" stroke-width="2"/>')
        body.append(f'<text x="{35 + index*170}" y="285" fill="{colors[index % 4]}" '
                    f'font-family="sans-serif">{label}</text>')
    body.append('</svg>')
    (OUT / name).write_text("".join(body), encoding="utf-8")


def diagram(name: str, title: str, labels: list[str]) -> None:
    text = " → ".join(labels)
    content = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="150">'
               '<rect width="100%" height="100%" fill="white"/>'
               f'<text x="20" y="35" font-family="sans-serif" font-size="20">{title}</text>'
               f'<text x="20" y="90" font-family="sans-serif" font-size="16">{text}</text></svg>')
    (OUT / name).write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rate, duration = 48_000, 0.5
    base = sine(440, duration, rate, 0.5)
    clipped = [max(-1, min(1, value * 3)) for value in base]
    low_bits = quantize(base, 4)
    stereo_right = sine(660, duration, rate, 0.5)
    write_pcm16(OUT / "tone-correct.wav", [base], rate)
    write_pcm16(OUT / "tone-wrong-metadata.wav", [base], 44_100)
    write_pcm16(OUT / "tone-4-bit-simulation.wav", [low_bits], rate)
    write_pcm16(OUT / "tone-clipped.wav", [clipped], rate)
    write_pcm16(OUT / "tone-stereo.wav", [base, stereo_right], rate)
    dense = sine(4, 1, 128, 0.8)
    sparse = sine(4, 1, 16, 0.8)
    alias_points = sine(11, 1, 16, 0.8)
    svg("frequency-amplitude-phase.svg", "Frequency, amplitude, and phase",
        [("4 Hz", dense), ("half amplitude", [v/2 for v in dense]),
         ("phase + pi/2", sine(4, 1, 128, 0.8, math.pi/2))])
    svg("sampled-sine.svg", "Continuous-looking curve and samples", [("reference", dense), ("16 sample/s", sparse)])
    svg("sample-rate-comparison.svg", "Same signal, different sample rates", [("128 sample/s", dense), ("16 sample/s", sparse)])
    svg("nyquist.svg", "Below, near, and above Nyquist (16 sample/s)",
        [("5 Hz", sine(5, 1, 16)), ("7 Hz", sine(7, 1, 16)), ("11 Hz", alias_points)])
    svg("aliasing.svg", "11 Hz sampled at 16 sample/s aliases", [("samples", alias_points), ("apparent 5 Hz", sine(-0 + 5, 1, 16, phase=math.pi))])
    svg("quantization.svg", "Original, 4-bit quantization, and error",
        [("original", base[:200]), ("4-bit", low_bits[:200]), ("error", [a-b for a,b in zip(base, low_bits)][:200])])
    svg("low-bit-depth.svg", "Low-bit-depth staircase", [("4-bit", low_bits[:300])])
    svg("pcm-samples.svg", "Successive PCM sample values", [("normalized PCM", base[:100])])
    svg("waveform-inspection.svg", "Whole waveform and zoomed samples", [("whole", base), ("zoom", base[:100])])
    diagram("acoustic-to-digital.svg", "Acoustic to digital", ["source", "pressure", "microphone", "signal", "ADC", "samples"])
    diagram("stereo-interleaving.svg", "Stereo interleaving", ["L0", "R0", "L1", "R1", "L2", "R2"])
    diagram("wav-structure.svg", "Simplified PCM WAV", ["RIFF/WAVE", "fmt chunk", "data chunk"])
    diagram("adc-dac-path.svg", "End-to-end path", ["sound", "mic", "ADC", "samples", "DAC", "amp", "speaker", "sound"])
    diagram("buffer-duration.svg", "Buffer duration", ["256 samples", "÷ 48,000 samples/s", "5.33 ms"])
    report = inspect_wav(OUT / "tone-stereo.wav")
    print(f"Generated 5 WAV and 13 SVG files in {OUT}")
    print(report)


if __name__ == "__main__":
    main()
