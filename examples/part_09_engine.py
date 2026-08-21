"""Part IX offline engine and deadline simulation; not a real-time benchmark."""
from pathlib import Path
from tech_music.engine import Message, MiniEngine, Session, simulate_deadlines
from tech_music.waveform import write_wav

ROOT = Path(__file__).resolve().parents[1]

def main():
    session = Session(sample_rate=16_000, block_size=256, duration_frames=8_000,
        events=[Message(120,0,"note_on",{"note":69,"velocity":.8}),
                Message(4_120,1,"note_off",{"note":69})])
    audio = MiniEngine(session).render()
    out = ROOT / "assets" / "part-09"; out.mkdir(parents=True, exist_ok=True)
    write_wav(out / "mini-engine.wav", audio, session.sample_rate)
    rows = simulate_deadlines([256]*3, session.sample_rate, [.002,.018,.004])
    print("block frames deadline_ms processing_ms margin_ms missed")
    for x in rows: print(x.index,x.frames,f"{x.buffer_seconds*1000:.3f}",f"{x.processing_seconds*1000:.3f}",f"{x.margin_seconds*1000:.3f}",x.missed)
    print("Educational simulation only; wrote", out / "mini-engine.wav")
if __name__ == "__main__": main()
