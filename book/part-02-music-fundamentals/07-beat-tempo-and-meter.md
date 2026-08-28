# Chapter 7 — Beat, Tempo, and Meter

![Chapter 7](../../images/chapters/7.png)

At 120 BPM, count four evenly spaced beats:

```text
beat 1 -> 0.0 seconds
beat 2 -> 0.5 seconds
beat 3 -> 1.0 seconds
beat 4 -> 1.5 seconds
```

This chapter turns that small listening example into a timeline that Python can
calculate, audio can make audible, and a debugger can inspect.

## Learning objectives

By the end of this chapter, you will be able to:

- distinguish pulse, beat, tempo, BPM, bar, time signature, meter, downbeat, and
  subdivision;
- convert BPM to seconds per beat and explain the units in the calculation;
- place beats and eighth-note subdivisions on a timeline in seconds;
- run the Part II musical sketch and interpret its WAV and SVG outputs;
- read `seconds_per_beat(...)` and `click_positions(...)` in the implementation;
- use a debugger and tests to diagnose an inverted tempo calculation.

## First mental model: evenly spaced markers on a timeline

Imagine a ruler whose units are seconds. A steady musical pulse places markers
at equal distances along that ruler. At 120 BPM, the distance between adjacent
beat markers is 0.5 seconds:

```text
seconds:  0.0---------0.5---------1.0---------1.5---------2.0
beats:     1           2           3           4        next bar
```

The ruler is measured time. The numbers `1, 2, 3, 4` are counted musical
positions. Software connects the two by storing beat positions as timestamps in
seconds.

## Why 120 BPM means 0.5 seconds per beat

**BPM** means beats per minute. Therefore 120 BPM means 120 beats occur during
one minute. One minute contains 60 seconds, so:

```text
seconds_per_beat = 60 / BPM
seconds_per_beat = 60 / 120
seconds_per_beat = 0.5
```

The units show why the ratio is oriented this way:

```text
60 seconds / minute
divided by
120 beats / minute
=
0.5 seconds / beat
```

Dividing fractions multiplies by the reciprocal. The `minute` units cancel,
leaving the unit we need: `seconds / beat`.

> **Engineering lesson:** Attach units to values before trusting a formula. A
> number can be valid Python while representing the wrong physical quantity.

## Build the vocabulary one idea at a time

### Pulse

A **pulse** is a recurring temporal reference that you can hear or feel as
regular motion. Tap your hand steadily on a desk. The recurring taps establish a
pulse even before you number them.

### Beat

A **beat** is a position in the pulse that we count and use to organize musical
events. In `1, 2, 3, 4`, each number identifies a beat. The pulse is the ongoing
regularity; a beat is one counted position within it.

### Tempo

**Tempo** is the rate of the beats. A slower tempo puts more time between beats;
a faster tempo puts less time between beats. Tempo describes rate, not a
particular beat position.

### BPM

**Beats per minute (BPM)** is a common numerical measurement of tempo. At 60
BPM, one beat lasts 1 second. At 120 BPM, one beat lasts 0.5 seconds. Doubling
the BPM halves the duration of each beat.

### Bar or measure

A **bar**, also called a **measure**, groups a recurring number of beats. Bar
lines make those groups visible:

```text
| 1   2   3   4 | 1   2   3   4 |
  bar 1            bar 2
```

The count restarts at `1`, but measured time continues forward.

### Time signature

A **time signature** is the written symbol that describes a notated beat
organization. In **4/4**, the upper `4` says that a bar contains four beats and
the lower `4` identifies the quarter note as the notated beat unit.

For this lesson, one 4/4 bar at 120 BPM lasts:

```text
4 beats * 0.5 seconds/beat = 2.0 seconds
```

### Meter

**Meter** is the heard organization of beats into recurring strong and weak
positions. It is not merely the printed time signature. A conventional 4/4
listening model gives beat 1 the strongest emphasis, beat 3 a secondary
emphasis, and beats 2 and 4 weaker positions:

```text
Beat:       1      2      3      4
Time:      0.0    0.5    1.0    1.5
Strength: strong  weak   medium weak
```

Real music can accent other positions. Those accents can play with the meter
rather than erase it.

### Downbeat

The **downbeat** is the first beat of a bar. In the timeline above, beat 1 at
`0.0` seconds is the first downbeat. The next bar's downbeat occurs at `2.0`
seconds.

### Subdivision

A **subdivision** divides each beat into smaller, regular positions. Divide each
beat into two equal parts and count eighth notes as `1 & 2 & 3 & 4 &`:

```text
Count:  1    &    2    &    3    &    4    &
Time:   0   .25  .50  .75  1.0  1.25  1.5  1.75
```

At 120 BPM a beat is 0.5 seconds long. Half of 0.5 is 0.25, so each `&` occurs
0.25 seconds after the numbered beat and 0.25 seconds before the next one. The
`&` is halfway between beats; it is not an extra beat.

## Try the experiment

This repository uses a `src` layout and is normally run from an activated
virtual environment. From the repository root, activate it if it is not already
active:

```bash
source .venv/bin/activate
```

Then generate the Part II sketch at 120 BPM:

```bash
python -m tech_music.music --bpm 120
```

Expected terminal output:

```text
Wrote assets/part-02/musical-sketch.wav and assets/part-02/arrangement.svg
```

The command creates two files:

1. Open `assets/part-02/musical-sketch.wav`, listen to the note attacks, and
   count `1-2-3-4` steadily. Do not expect a metronome-only click track: this is
   the capstone musical sketch, whose events use the same tempo conversion.
2. Open `assets/part-02/arrangement.svg`. Read it from left to right. Horizontal
   position means elapsed time, and equal-width two-bar sections mean equal
   durations. At 120 BPM, each 4/4 bar lasts 2 seconds, each displayed two-bar
   section lasts 4 seconds, and the eight-bar arrangement spans 16 seconds.

The SVG shows large arrangement regions rather than drawing every beat. Mentally
place four equal beat positions inside each bar: the same seconds-per-beat
calculation controls the finer timeline.

### Predict, then rerun

Before running anything else, predict:

- Which tempo will sound slowest: 60, 90, or 150 BPM?
- Which will sound fastest?
- How many seconds will one beat last at each tempo?

Now run all three versions. Each run overwrites the same two output files, so
listen or copy a version before running the next command.

```bash
python -m tech_music.music --bpm 60
python -m tech_music.music --bpm 90
python -m tech_music.music --bpm 150
```

Expected results:

| Tempo | Calculation | Seconds per beat | Listening prediction |
| ---: | ---: | ---: | --- |
| 60 BPM | `60 / 60` | `1.0` | slowest |
| 90 BPM | `60 / 90` | about `0.667` | between the others |
| 150 BPM | `60 / 150` | `0.4` | fastest |

Observe that the event order and arrangement design remain the same. Only the
mapping from beat positions to seconds changes.

## Read and execute the conversion

Open `src/tech_music/music.py` and find this implementation:

```python
def seconds_per_beat(bpm: float) -> float:
    """Convert beats per minute to seconds per beat."""
    if bpm <= 0:
        raise ValueError("bpm must be positive")
    return 60.0 / bpm
```

Read it line by line:

1. `bpm: float` accepts a numeric tempo, and `-> float` documents a numeric
   result that may contain a fractional second.
2. The docstring states the conversion and, importantly, its output unit.
3. `if bpm <= 0` rejects a tempo that cannot describe forward beat spacing.
4. `60.0 / bpm` divides seconds per minute by beats per minute and returns
   seconds per beat.

Run the function directly from the repository root:

```bash
python - <<'PY'
from tech_music.music import seconds_per_beat

for bpm in (60, 90, 120, 150):
    print(bpm, seconds_per_beat(bpm))
PY
```

Expected output:

```text
60 1.0
90 0.6666666666666666
120 0.5
150 0.4
```

The long value for 90 BPM is normal floating-point representation. It means
two-thirds of a second to the available precision.

## Turn one duration into many beat positions

The next function builds a timeline:

```python
def click_positions(bpm: float, beats: int) -> list[float]:
    """Return beat timestamps starting at the downbeat (time zero)."""
    if beats < 1:
        raise ValueError("beats must be positive")
    beat = seconds_per_beat(bpm)
    return [index * beat for index in range(beats)]
```

`beat` stores the spacing between adjacent beat positions. `range(beats)`
produces zero-based indices. Multiplying each index by the spacing is equivalent
to repeatedly adding seconds per beat:

```text
index 0: 0 * 0.5 = 0.0
index 1: 1 * 0.5 = 0.5
index 2: 2 * 0.5 = 1.0
index 3: 3 * 0.5 = 1.5
```

Execute it:

```bash
python - <<'PY'
from tech_music.music import click_positions

print(click_positions(120, 4))
PY
```

Expected output:

```text
[0.0, 0.5, 1.0, 1.5]
```

Notice that four beats have four onset timestamps; the list does not include
the next bar's downbeat at 2.0 seconds.

| Layer | Representation |
| --- | --- |
| Music concept | beat positions |
| Software representation | floating-point timestamps in seconds |
| Future application | sequencer events, MIDI timing, and DAW timeline regions |

> **Music-and-engineering lesson:** A beat grid is relational, while a rendered
> audio timeline needs measured time. Tempo is the conversion boundary between
> those representations.

## Debugging Laboratory — The tempo is wrong

In this laboratory, the program still runs and creates valid files, but one
reversed ratio makes every downstream event occur at the wrong time.

### Goal

Use runtime values and dimensional reasoning to diagnose a tempo conversion bug,
then restore the implementation and confirm it with an automated test.

### Open the Source

Open `src/tech_music/music.py` in VS Code and locate
`seconds_per_beat`. Also locate the call to it inside `click_positions`.

### Set the Breakpoint

Click in the editor gutter beside this operation in `seconds_per_beat`:

```python
return 60.0 / bpm
```

Also set a breakpoint beside the return operation in `click_positions`. The
first breakpoint exposes the conversion; the second lets you inspect the
timestamps created from it.

### Launch the Debugger

The repository includes a VS Code launch configuration for this laboratory:

1. Open the Command Palette and choose **Python: Select Interpreter**; select
   the interpreter in `.venv`.
2. Open **Run and Debug**.
3. Select **Chapter 7: music module at 120 BPM**.
4. Press **F5** and continue until the breakpoint in `seconds_per_beat` is
   reached.

The configuration launches the package as `python -m tech_music.music --bpm
120`. Launching it as a module matters because `music.py` uses package-relative
imports.

Use **Step Over** to evaluate the current operation, **Continue** to reach later
calls, and the **Variables** or **Watch** panel to inspect expressions. Because
the renderer calls the conversion directly, add these Watch expressions while
paused:

```text
bpm
60.0 / bpm
click_positions(120, 4)
```

The last expression is best evaluated in the Debug Console after stepping out
of `seconds_per_beat`; evaluating it while stopped inside that same function can
re-enter the breakpoint.

### Observe

At 120 BPM, record these values:

```text
bpm                         120.0
seconds-per-beat result       0.5
click_positions(120, 4)       [0.0, 0.5, 1.0, 1.5]
```

Ask what unit belongs to each value. `bpm` has units of beats/minute, the result
has seconds/beat, and each list item is a timestamp in seconds from the
downbeat.

You can inspect the smaller call without rendering audio by entering this in
the Debug Console:

```python
click_positions(120, 4)
```

Use **Step Into** at the call if you want to follow the sequence
`click_positions` -> `seconds_per_beat` -> list comprehension.

### Introduce the Bug

Temporarily change only the final line of `seconds_per_beat`:

```python
return bpm / 60.0
```

Before executing it, predict the returned value and the four timestamps. Then
run:

```bash
python - <<'PY'
from tech_music.music import click_positions, seconds_per_beat

print(seconds_per_beat(120))
print(click_positions(120, 4))
PY
```

Broken output:

```text
2.0
[0.0, 2.0, 4.0, 6.0]
```

The broken spacing is 2.0 seconds rather than 0.5 seconds. Each interval is
`2.0 / 0.5 = 4` times as long, so the result is **four times slower** than the
correct beat spacing at 120 BPM. Calling it “twice too fast” would be incorrect.

Run the complete experiment once with the bug if you want to hear its downstream
effect:

```bash
python -m tech_music.music --bpm 120
```

The files are still syntactically valid. Their musical timing is wrong. That is
why successful execution is not sufficient evidence of correctness.

### Diagnose with units

Write the broken expression with its units:

```text
bpm / 60
=
beats/minute / seconds/minute
=
beats/second
```

That yields a rate in beats per second, not a duration in seconds per beat. The
function promises the reciprocal quantity.

### Repair and verify

Restore the source before continuing:

```python
return 60.0 / bpm
```

Then run the focused test:

```bash
python -m pytest tests/test_music.py::test_tempo_reference_points
```

Expected result includes:

```text
4 passed
```

The reference points confirm, among other tempos, that:

```python
seconds_per_beat(120) == 0.5
click_positions(120, 4) == [0.0, 0.5, 1.0, 1.5]
```

If the inverted expression returns, this test fails deterministically before a
listener has to notice that a whole render is mistimed.

## What you should understand before moving on

Answer these without memorizing the chapter's prose. Draw a timeline or derive
the units when useful.

1. What does 120 BPM mean?
2. Why is one beat at 120 BPM 0.5 seconds?
3. What is the difference between beat and tempo?
4. What does 4/4 tell us?
5. What is meter beyond the written time signature?
6. What is a subdivision?
7. How does software represent beat positions?
8. What goes wrong downstream if the BPM-to-seconds conversion is wrong?

If you can calculate the four timestamps, count them against the WAV, locate
them conceptually in the SVG timeline, and explain the conversion's units, you
are ready to continue.

## Forward connection

Chapter 8 places rhythms on subdivisions and then introduces swing and
microtiming. Later chapters attach pitches and durations to sequencer events;
MIDI systems schedule musical data; and DAWs display bars, beats, and regions on
a horizontal timeline. Each layer depends on the conversion you debugged here.

## References

Numbers refer to the [project bibliography](../../references/bibliography.md):
Butler [19] on meter in electronic dance music; Laitz [24] on meter and
notation; Python `wave` [1] for generated audio.
