import json
import math
import random

import pytest

from tech_music.generative import (AdaptiveConfig, MODES, NoteEvent, decode_events,
    encode_events, euclidean_pattern, generate, markov_sequence, regenerate, render,
    to_session, weighted_choice)


def test_seeded_generation_is_reproducible_and_serializable():
    config = AdaptiveConfig(seed=42, duration=4)
    assert generate(config) == generate(AdaptiveConfig.from_json(config.to_json()))
    assert json.loads(config.to_json())["seed"] == 42


@pytest.mark.parametrize("mode", MODES)
def test_modes_generate_ordered_valid_bounded_events(mode):
    result = generate(AdaptiveConfig(mode=mode, duration=3, tempo_min=60, tempo_max=140))
    assert result.patch
    assert list(result.events) == sorted(result.events)
    for event in result.events:
        event.validate(3)
        assert (event.note - result.config.root) % 12 in {0, 2, 3, 5, 7, 8, 10}


def test_validation_rejects_unknown_mode_ranges_and_incompatible_tempo():
    with pytest.raises(ValueError, match="unknown mode"): generate(AdaptiveConfig(mode="magic"))
    with pytest.raises(ValueError, match="density"): generate(AdaptiveConfig(density=1.1))
    with pytest.raises(ValueError, match="does not overlap"):
        generate(AdaptiveConfig(mode="deep-focus", tempo_min=120, tempo_max=130))


def test_weight_and_markov_validation_and_seed():
    with pytest.raises(ValueError): weighted_choice(random.Random(1), {"a": 0, "b": 0})
    with pytest.raises(ValueError): weighted_choice(random.Random(1), {"a": -1})
    transitions = {"C": {"G": .6, "F": .4}, "G": {"C": 1}, "F": {"C": 1}}
    assert markov_sequence(transitions, "C", 8, 7) == markov_sequence(transitions, "C", 8, 7)
    with pytest.raises(ValueError, match="missing"): markov_sequence({"C": {"X": 1}}, "C", 3, 1)


def test_euclidean_and_token_round_trip():
    pattern = euclidean_pattern(5, 8)
    assert len(pattern) == 8 and sum(pattern) == 5
    events = [NoteEvent(0, .25, 60), NoteEvent(.5, .2, 63, .5, "bass")]
    assert decode_events(encode_events(events)) == events
    with pytest.raises(ValueError): decode_events(["NOTE_60"])


def test_human_loop_locks_and_adapts():
    first = generate(AdaptiveConfig(seed=1, duration=3))
    changed = regenerate(first, lock_events=True, seed=2)
    assert changed.events == first.events
    assert changed.config.seed == 2
    assert generate(AdaptiveConfig(mode="exploration", seed=1, duration=3)) != first


def test_end_to_end_session_and_render_contract():
    generation = generate(AdaptiveConfig(seed=9, duration=2))
    session = to_session(generation)
    audio = render(generation)
    assert session.validate() == []
    assert len(audio) == 16_001
    assert all(math.isfinite(x) for x in audio)
    assert max(map(abs, audio), default=0) <= 1
