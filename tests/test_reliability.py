"""
Tests for src/reliability.py.

Run with:  pytest tests/test_reliability.py
"""

from src.reliability import (
    validate_user_preferences,
    assess_recommendation_reliability,
)


# A standard valid profile we can reuse in several tests
VALID_PREFS = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
}


def make_recommendations(top_score):
    """
    Build a small fake recommendation list in the same format that
    recommend_songs() returns: a list of (song_dict, score, explanation).
    The first item has the given top_score, and the second is lower.
    """
    song_a = {"title": "Song A", "genre": "pop", "mood": "happy", "energy": 0.8}
    song_b = {"title": "Song B", "genre": "rock", "mood": "intense", "energy": 0.9}
    return [
        (song_a, top_score, "test explanation"),
        (song_b, top_score - 1.0, "test explanation"),
    ]


# ---------- validate_user_preferences() ----------

def test_valid_profile_passes_validation():
    is_valid, message = validate_user_preferences(VALID_PREFS)
    assert is_valid is True
    assert message != ""


def test_empty_genre_fails_validation():
    prefs = {"favorite_genre": "", "favorite_mood": "happy", "target_energy": 0.80}
    is_valid, message = validate_user_preferences(prefs)
    assert is_valid is False
    assert "favorite_genre" in message


def test_energy_above_range_fails_validation():
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 1.5}
    is_valid, message = validate_user_preferences(prefs)
    assert is_valid is False
    assert "target_energy" in message


# ---------- assess_recommendation_reliability() ----------

def test_high_reliability_when_top_score_is_3_5():
    result = assess_recommendation_reliability(VALID_PREFS, make_recommendations(3.5))
    assert result["level"] == "High"


def test_medium_reliability_when_top_score_is_2_5():
    result = assess_recommendation_reliability(VALID_PREFS, make_recommendations(2.5))
    assert result["level"] == "Medium"


def test_low_reliability_when_top_score_is_1_5():
    result = assess_recommendation_reliability(VALID_PREFS, make_recommendations(1.5))
    assert result["level"] == "Low"


def test_empty_recommendation_list_is_low_reliability():
    result = assess_recommendation_reliability(VALID_PREFS, [])
    assert result["level"] == "Low"
    assert result["message"] != ""
