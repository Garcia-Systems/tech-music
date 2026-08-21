from pathlib import Path
import pytest
from scripts.summarize_listening import summarize
HEADER="condition,concentration,distraction,enjoyment,fatigue,urge_to_change,music_awareness,task_difficulty,desire_to_continue\n"
def test_summary_groups_and_averages(tmp_path: Path):
    path=tmp_path/'notes.csv'; path.write_text(HEADER+'silence,3,1,4,2,1,2,3,4\nsilence,5,1,2,2,1,2,3,4\n')
    assert summarize(path)['silence']['concentration'] == 4

def test_summary_rejects_rating_outside_scale(tmp_path: Path):
    path=tmp_path/'notes.csv'; path.write_text(HEADER+'music,6,1,2,2,1,2,3,4\n')
    with pytest.raises(ValueError, match='1–5'): summarize(path)
