"""Intentionally wrong: diagnose this exercise before reading the solution."""
import math

def broken_sine_wave(frequency=440.0, duration=1.0, sample_rate=44_100):
    time_seconds = range(round(duration * sample_rate))  # BUG: what unit is this?
    return [0.5 * math.sin(2 * math.pi * frequency * t) for t in time_seconds]
