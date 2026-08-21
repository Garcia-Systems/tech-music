"""Capstone debugging input: valid Python, musically inconsistent data."""
from tech_music.music import NoteEvent

BPM = 240  # Clue: requested design tempo was 120.
SCALE = {60, 62, 64, 65, 67, 69, 71, 72}
KICK_STEPS = [0, 4, 9, 12]  # One onset misses the quarter-note grid.
CHORD = [60, 65, 67]  # Intended label: C major.
BASS_ENTRY = 4  # Intended arrangement: bass enters at beat 8.
SECTION_BARS = [2, 2, 3, 2]  # The design has four equal sections.
MELODY = [NoteEvent(60, 8, 1), NoteEvent(63, 9, 1), NoteEvent(64, 10, 2)]

print(BPM, SCALE, KICK_STEPS, CHORD, BASS_ENTRY, SECTION_BARS, MELODY)
