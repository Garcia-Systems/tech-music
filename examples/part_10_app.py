"""Render every Part X capstone artifact from one project model."""
from pathlib import Path
from tech_music.app import diagnostic_text, load_project, plot_project, render_project
from tech_music.waveform import write_wav
ROOT=Path(__file__).resolve().parents[1]
def main():
    project=load_project(ROOT/'data/part-10-project.json')
    audio,report=render_project(project)
    generated=ROOT/'generated'
    audio_directory=generated/'audio'/'part-10'
    plot_directory=generated/'plots'/'part-10'
    report_directory=generated/'reports'/'part-10'
    audio_directory.mkdir(parents=True,exist_ok=True)
    report_directory.mkdir(parents=True,exist_ok=True)
    write_wav(audio_directory/'boundary-signals.wav',audio,project['sample_rate_hz'])
    plot_project(project,audio,plot_directory)
    (report_directory/'diagnostics.txt').write_text(diagnostic_text(project,report),encoding='utf-8')
    print(diagnostic_text(project,report),end='')
if __name__=='__main__': main()
