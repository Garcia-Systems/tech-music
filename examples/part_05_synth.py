"""Generate the Part V listening examples, diagrams, and capstone render."""
from pathlib import Path
import math

from tech_music.synth import (ADSR, SynthNote, additive_tone, adsr_envelope,
                              fm_tone, lfo, load_patch, one_pole_lowpass,
                              oscillator, render_capstone, render_sequence)
from tech_music.waveform import write_wav

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "part-05"


def svg_plot(path: Path, title: str, series: list[tuple[str, list[float]]]) -> None:
    width, height, pad = 900, 320, 45
    colors = ("#1769aa", "#c23b22", "#228b22", "#7b2cbf")
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="450" y="24" text-anchor="middle" font-family="sans-serif">{title}</text>',
             f'<line x1="{pad}" y1="160" x2="{width-pad}" y2="160" stroke="#aaa"/>']
    for row, (label, values) in enumerate(series):
        shown = values[:1000]
        points = " ".join(f"{pad+i*(width-2*pad)/max(1,len(shown)-1):.2f},{160-v*105:.2f}"
                          for i, v in enumerate(shown))
        parts += [f'<polyline points="{points}" fill="none" stroke="{colors[row % 4]}"/>',
                  f'<text x="{55+row*180}" y="300" fill="{colors[row % 4]}" font-family="sans-serif">{label}</text>']
    path.write_text("".join(parts) + "</svg>\n", encoding="utf-8")


def architecture_svg() -> None:
    labels = ["Note event", "Voice allocator", "Oscillator", "Envelope", "Filter",
              "Amplifier", "Voice mix", "Audio buffer", "Output"]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="150">',
             '<rect width="100%" height="100%" fill="white"/>']
    for i, label in enumerate(labels):
        x = 10 + i * 120
        parts += [f'<rect x="{x}" y="45" width="100" height="45" rx="6" fill="#e8f1fa" stroke="#1769aa"/>',
                  f'<text x="{x+50}" y="72" text-anchor="middle" font-size="12" font-family="sans-serif">{label}</text>']
        if i < len(labels)-1:
            parts.append(f'<path d="M{x+100} 67 H{x+118}" stroke="#333" marker-end="url(#a)"/>')
    parts.insert(2, '<defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6z"/></marker></defs>')
    (OUT / "synth-architecture.svg").write_text("".join(parts)+"</svg>\n", encoding="utf-8")


def spectrum_svg(path: Path, title: str, signals: list[tuple[str, list[float]]],
                 sample_rate: int) -> None:
    """Plot a deliberately small direct-DFT preview without teaching the derivation."""
    size, bins = 1024, 120
    spectra = []
    for label, signal in signals:
        data = signal[:size]
        magnitudes = []
        for k in range(bins):
            real = sum(x * math.cos(2*math.pi*k*n/size) for n,x in enumerate(data))
            imag = -sum(x * math.sin(2*math.pi*k*n/size) for n,x in enumerate(data))
            magnitudes.append(math.hypot(real, imag))
        peak = max(magnitudes) or 1
        spectra.append((label, [value/peak for value in magnitudes]))
    svg_plot(path, f"{title} (0–{sample_rate*bins/size:.0f} Hz preview)", spectra)


def state_diagram(path: Path, title: str, rows: list[str]) -> None:
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="700" height="260">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="350" y="25" text-anchor="middle" font-family="sans-serif">{title}</text>']
    for i, row in enumerate(rows):
        parts += [f'<rect x="80" y="{45+i*48}" width="540" height="34" rx="5" fill="#e8f1fa" stroke="#1769aa"/>',
                  f'<text x="350" y="{67+i*48}" text-anchor="middle" font-family="sans-serif">{row}</text>']
    path.write_text("".join(parts)+"</svg>\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rate = 22_050
    waves = [(name, oscillator(220, 1, rate, .45, waveform=name))
             for name in ("sine", "square", "saw", "triangle")]
    for name, samples in waves:
        write_wav(OUT / f"waveform-{name}.wav", samples, rate)
    svg_plot(OUT / "waveforms.svg", "One frequency, four waveforms",
             [(name, samples[:401]) for name, samples in waves])
    env = ADSR(.08, .15, .55, .25)
    curve = adsr_envelope(.7, env, rate)
    raw = oscillator(220, len(curve)/rate, rate, .5)
    shaped = [a*b for a, b in zip(raw, curve)]
    write_wav(OUT / "envelope-shaped.wav", shaped, rate)
    svg_plot(OUT / "adsr.svg", "ADSR envelope", [("level", curve[::20])])
    source = oscillator(110, 1, rate, .5, waveform="saw")
    filtered = one_pole_lowpass(source, 700, rate)
    write_wav(OUT / "filter-before-after.wav", source + filtered, rate)
    svg_plot(OUT / "filter-comparison.svg", "Saw: source and low-pass output",
             [("source", source[:500]), ("filtered", filtered[:500])])
    spectrum_svg(OUT / "filter-spectrum.svg", "Low-pass before / after spectrum",
                 [("source", source), ("filtered", filtered)], rate)
    modulation = lfo(4, 1, rate, .5)
    svg_plot(OUT / "modulation.svg", "LFO and amplitude destination",
             [("LFO", modulation[::25]), ("gain", [(x+1)/2 for x in modulation[::25]])])
    detuned = [(a+b)*.5 for a,b in zip(oscillator(220, 2, rate, .45), oscillator(222, 2, rate, .45))]
    write_wav(OUT / "detuned-beating.wav", detuned, rate)
    svg_plot(OUT / "oscillator-mix.svg", "Two slightly detuned oscillators", [("mix", detuned[::20])])
    additive = additive_tone(110, [1, .5, .33, .25, .2], 1, rate)
    fm = fm_tone(220, 110, 90, 1, rate)
    write_wav(OUT / "additive.wav", additive, rate); write_wav(OUT / "fm.wav", fm, rate)
    svg_plot(OUT / "harmonic-preview.svg", "Additive harmonics: time-domain preview", [("sum", additive[:800])])
    spectrum_svg(OUT / "harmonic-spectrum.svg", "Five-harmonic additive spectrum",
                 [("sum", additive)], rate)
    architecture_svg()
    state_diagram(OUT / "patch-architecture.svg", "Patch architecture", [
        "version + validated parameters", "oscillator + LFO", "ADSR + low-pass", "rendered note"])
    state_diagram(OUT / "voice-allocation.svg", "Two-voice allocation example", [
        "note_on 60 → voice 1", "note_on 64 → voice 2", "note_on 67 → steal oldest voice", "note_off 64 → release/remove"])
    render_capstone(ROOT / "data" / "part-05-patch.json", OUT / "capstone.wav", rate)
    patch = load_patch(ROOT / "data" / "part-05-patch.json")
    chord = render_sequence(patch, [SynthNote(n, 0, 1) for n in (60,64,67)], rate)
    write_wav(OUT / "polyphonic-chord.wav", chord, rate)
    print(f"Generated {len(list(OUT.glob('*.wav')))} WAV files and "
          f"{len(list(OUT.glob('*.svg')))} SVG files in {OUT}")


if __name__ == "__main__":
    main()
