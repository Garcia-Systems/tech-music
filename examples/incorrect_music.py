"""Intentionally wrong Part II calculations: investigate before fixing."""


def seconds_per_beat(bpm: float) -> float:
    return bpm / 60  # BUG: ratio and units are inverted.


def octave_frequency(note: int) -> float:
    return 440 * 2 ** ((note - 69) / 6)  # BUG: an octave has 12 semitones.


def major_triad(root: int) -> list[int]:
    return [root + interval for interval in (0, 5, 7)]  # BUG: wrong third.


snare = [0, 0, 0, 0, 1, 0, 0, 0]
print("120 BPM interval:", seconds_per_beat(120))
print("A5 frequency:", octave_frequency(81))
print("C major?:", major_triad(60))
print("Human step 5 selected as index 5?:", snare[5])  # BUG: zero-based index.
