"""Generate Part VIII event, MIDI, audio, and SVG teaching artifacts."""
from __future__ import annotations

import json
import math
from pathlib import Path

from tech_music.midi import (MidiEvent, Router, TempoEvent, bend_frequency,
    quantize_tick, schedule, swing_tick, tick_to_seconds, write_midi_file)
from tech_music.synth import ADSR, Patch
from tech_music.waveform import write_wav

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "part-08"
RATE, PPQ = 16_000, 480
TEMPO = [TempoEvent(0, 120)]
SINE = Patch("sine", .45, ADSR(.005, .04, .75, .08), 3500)
SAW = Patch("saw", .25, ADSR(.005, .05, .55, .1), 1300)


def notes(onsets, pitches=(60, 64, 67, 72), duration=360, channel=0, velocities=None):
    events = []
    for i, (tick, note) in enumerate(zip(onsets, pitches)):
        velocity = (velocities or [90] * len(onsets))[i]
        events += [MidiEvent(tick, "note_on", channel, note, velocity, order=2*i),
                   MidiEvent(tick + duration, "note_off", channel, note, 0, order=2*i+1)]
    return events


def plot(name, title, series, y_label="value"):
    width, height = 800, 320
    colors = ["#2563eb", "#dc2626", "#059669"]
    all_points = [point for _, points in series for point in points]
    xmax = max((x for x, _ in all_points), default=1); ys = [y for _, y in all_points]
    ymin, ymax = min(ys, default=0), max(ys, default=1)
    span = max(ymax-ymin, 1e-9)
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
            '<rect width="100%" height="100%" fill="white"/>',
            f'<text x="25" y="28" font-family="sans-serif" font-size="18">{title}</text>',
            f'<text x="8" y="165" font-family="sans-serif" font-size="12">{y_label}</text>',
            '<line x1="45" y1="270" x2="770" y2="270" stroke="#777"/>']
    for index, (label, points) in enumerate(series):
        coordinates = " ".join(f"{45+725*x/max(xmax,1):.1f},{270-210*(y-ymin)/span:.1f}" for x,y in points)
        body += [f'<polyline points="{coordinates}" fill="none" stroke="{colors[index%3]}" stroke-width="2"/>',
                 f'<text x="{50+index*210}" y="305" fill="{colors[index%3]}" font-family="sans-serif">{label}</text>']
    (OUT/name).write_text("".join(body)+"</svg>\n", encoding="utf-8")


def flow(name, title, labels):
    y, items = 45, [f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{70*len(labels)+40}">',
        '<rect width="100%" height="100%" fill="white"/>', f'<text x="25" y="25" font-family="sans-serif" font-size="18">{title}</text>']
    for i, label in enumerate(labels):
        items += [f'<rect x="220" y="{y}" width="360" height="35" rx="8" fill="#dbeafe" stroke="#2563eb"/>',
                  f'<text x="400" y="{y+23}" text-anchor="middle" font-family="sans-serif">{label}</text>']
        if i < len(labels)-1: items.append(f'<text x="400" y="{y+55}" text-anchor="middle" font-size="24">↓</text>')
        y += 70
    (OUT/name).write_text("".join(items)+"</svg>\n", encoding="utf-8")


def render(name, events, patches=None, tempos=TEMPO):
    audio = Router(patches or {0: SINE}).route(events, tempos, PPQ, RATE)
    write_wav(OUT/f"{name}.wav", audio, RATE)
    return audio


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = notes([0, 480, 960, 1440])
    irregular = notes([25, 445, 1002, 1405])
    quantized = [MidiEvent(quantize_tick(e.tick, 120), e.type, e.channel, e.note,
                           e.velocity, order=e.order) for e in irregular]
    straight = notes([0, 240, 480, 720, 960, 1200, 1440, 1680], (60,62,64,65,67,69,71,72), 170)
    swung = [MidiEvent(swing_tick(e.tick, 240), e.type, e.channel, e.note, e.velocity, order=e.order)
             for e in straight]
    velocity = notes([0, 480, 960, 1440], (69,)*4, 360, velocities=[30,60,90,120])
    controls = [MidiEvent(0, "control_change", controller=7, value=25),
                *notes([0], (60,), 360), MidiEvent(480, "control_change", controller=7, value=110),
                *notes([480], (64,), 360)]
    for name, events in [("velocity-comparison", velocity), ("unquantized", irregular),
                         ("quantized", quantized), ("straight", straight), ("swung", swung),
                         ("controller-amplitude", controls), ("same-events-sine", base)]: render(name, events)
    render("same-events-saw", base, {0: SAW})
    # Pitch-bend listening is rendered as short notes following the displayed curve.
    bend_notes = []
    for i, bend in enumerate([-8192, -4096, 0, 4096, 8191]):
        approximate_note = round(69 + 2*bend/(8192 if bend < 0 else 8191))
        bend_notes += notes([i*360], (approximate_note,), 300)
    render("pitch-bend-steps", bend_notes)
    write_midi_file(OUT/"phrase.mid", base)
    (OUT/"phrase-events.json").write_text(json.dumps([e.__dict__ for e in base], indent=2)+"\n")
    plot("note-lifecycle.svg", "Note lifecycle / active voice", [("gate", [(0,0),(0,1),(.5,1),(.5,0),(.7,0)])])
    plot("note-number-mapping.svg", "MIDI note number to 12-TET frequency", [("frequency", [(n, 440*2**((n-69)/12)) for n in range(48,82)])], "Hz")
    plot("controller-curve.svg", "CC values (receiver maps CC 7 to amplitude)", [("CC 7", [(0,25),(480,25),(480,110),(960,110)])])
    bends=[-8192,-4096,0,4096,8191]
    plot("pitch-bend.svg", "Configured ±2-semitone bend", [("frequency", [(i,bend_frequency(69,b,2)) for i,b in enumerate(bends)])], "Hz")
    plot("ticks-beats-time.svg", "ticks → beats → seconds", [("ticks", [(i,i*480) for i in range(5)]),("milliseconds",[(i,1000*tick_to_seconds(i*480,TEMPO)) for i in range(5)])])
    plot("piano-roll.svg", "Piano roll: event data, not MIDI itself", [("notes", [(e.tick,e.note) for e in base if e.type=="note_on"])], "note")
    plot("quantization.svg", "Original and quantized onsets", [("original",[(i,t) for i,t in enumerate([25,445,1002,1405])]),("quantized",[(i,quantize_tick(t,120)) for i,t in enumerate([25,445,1002,1405])])], "tick")
    plot("swing.svg", "Straight and educational 2:1 swing", [("straight",[(i,i*240) for i in range(8)]),("swung",[(i,swing_tick(i*240,240)) for i in range(8)])], "tick")
    tempo_map=[TempoEvent(0,120),TempoEvent(960,90)]
    plot("tempo-map.svg", "Piecewise-constant tempo map", [("BPM",[(0,120),(959,120),(960,90),(1920,90)])], "BPM")
    flow("channel-routing.svg", "Channel routing", ["Channel 1 (API 0) / Channel 2 (API 1)", "Explicit route table", "Sine patch / Saw patch", "Audio mix"])
    flow("midi-routing.svg", "Where does the event stop?", ["Controller", "DAW / sequencer", "MIDI track and port", "Synthesizer", "Audio bus", "Speakers"])
    flow("midi-vs-audio.svg", "Related, not interchangeable", ["Musical intent: C-major chord", "Events: note_on 60, 64, 67", "Instrument renders", "Audio samples: 0.0, 0.02, 0.06 …"])
    flow("sequencer-architecture.svg", "Mini sequencer data flow", ["Sequence data", "Validation", "Timing conversion", "Deterministic scheduler", "Event router", "Synthesizer", "DSP", "Audio samples", "WAV"])
    print("Generated 9 WAV, 13 SVG, 1 MIDI, and 1 JSON artifact in", OUT)


if __name__ == "__main__": main()
