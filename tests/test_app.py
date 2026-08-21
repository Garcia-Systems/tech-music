import json
import math
import wave
from pathlib import Path
import pytest
from tech_music.app import (Tempo, automation_value, load_project, main, plot_project,
                            render_project, save_project, schedule_steps, validate_project)
from tech_music.dsp import FeedbackDelay, process_blocks

ROOT=Path(__file__).parents[1]
PROJECT=ROOT/'data/part-10-project.json'

def test_tempo_units_and_steps_are_deterministic():
    tempo=Tempo(120)
    assert tempo.beats_to_seconds(4)==2
    assert tempo.beats_to_sample_offset(1,8000)==4000
    assert tempo.ticks_to_beats(480)==1
    events=schedule_steps({'kick':[1,0,1,0], 'hat':[0,1,0,1]},120,2,2)
    assert [e['beat'] for e in events]==[0,.5,1,1.5,2,2.5,3,3.5]

def test_automation_interpolates_and_rejects_duplicate_boundaries():
    points=[{'beat':0,'value':0},{'beat':2,'value':1}]
    assert automation_value(points,1)==.5
    assert automation_value(points,4)==1
    with pytest.raises(ValueError): automation_value([{'beat':1,'value':0},{'beat':1,'value':1}],1.1)

def test_delay_state_persists_across_blocks():
    delay=FeedbackDelay(3,0,mix=1)
    assert process_blocks(delay,[1,0,0,0,0],2)==[0,0,0,1,0]

def test_session_round_trip_and_validation(tmp_path):
    project=load_project(PROJECT); destination=tmp_path/'copy.json'
    save_project(project,destination)
    assert load_project(destination)==project
    assert validate_project(project)==[]
    errors=validate_project(load_project(ROOT/'data/part-10-broken-project.json'))
    assert any('unknown patch' in e for e in errors)
    assert any('disconnected' in e for e in errors) or any('does not exist' in e for e in errors)

def test_complete_pipeline_is_deterministic_and_writes_wav(tmp_path):
    project=load_project(PROJECT)
    first,report=render_project(project,block_size=127); second,_=render_project(project,block_size=256)
    assert first==second
    assert report['track_count']==4 and report['event_count']==24
    assert len(first)==32000 and report['duration_seconds']==4
    assert 0 < report['peak'] <= 1
    output=tmp_path/'render.wav'
    assert main(['render',str(PROJECT),str(output)])==0
    with wave.open(str(output)) as wav: assert wav.getframerate()==8000 and wav.getnframes()==32000

def test_cli_validation_and_four_visualizations(tmp_path,capsys):
    assert main(['validate',str(PROJECT)])==0
    assert 'valid' in capsys.readouterr().out
    assert main(['validate',str(ROOT/'data/part-10-broken-project.json')])==1
    project=load_project(PROJECT); audio,_=render_project(project)
    paths=plot_project(project,audio,tmp_path)
    assert len(paths)==4 and all(p.read_text().startswith('<svg') for p in paths)
