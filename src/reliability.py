"""
Reliability checks for VibeMatch AI.

This module adds two simple safety layers around the recommender:

1. validate_user_preferences() checks the user's input BEFORE we recommend.
2. assess_recommendation_reliability() rates how confident we can be in
   the results AFTER we recommend.

No external AI APIs are used. Everything is plain, rule-based Python.
"""

from typing import Dict, List, Tuple


# Score thresholds used to decide the reliability level.
# Max possible score from score_song() is 4.0:
#   genre match (+2.0) + mood match (+1.0) + energy similarity (up to +1.0)
HIGH_RELIABILITY_THRESHOLD = 3.0
MEDIUM_RELIABILITY_THRESHOLD = 2.0


def validate_user_preferences(user_prefs: Dict) -> Tuple[bool, str]:
    """
    Check that the user's preferences are complete and sensible.

    Returns a tuple (is_valid, message):
      - (True, "success message") if everything looks good
      - (False, "explanation of the problem") if something is wrong
    """
    # The preferences must be a dictionary so we can look up keys
    if not isinstance(user_prefs, dict):
        return False, "User preferences must be a dictionary."

    # Check favorite_genre: must be a string that is not empty or just spaces
    genre = user_prefs.get("favorite_genre")
    if not isinstance(genre, str) or genre.strip() == "":
        return False, "favorite_genre must be a non-empty string (for example, 'pop')."

    # Check favorite_mood: must be a string that is not empty or just spaces
    mood = user_prefs.get("favorite_mood")
    if not isinstance(mood, str) or mood.strip() == "":
        return False, "favorite_mood must be a non-empty string (for example, 'happy')."

    # Check target_energy: must be a number (int or float).
    # Note: in Python, True/False count as ints, so we reject booleans explicitly.
    energy = user_prefs.get("target_energy")
    if isinstance(energy, bool) or not isinstance(energy, (int, float)):
        return False, "target_energy must be a number between 0.0 and 1.0."

    # Check target_energy is inside the allowed range
    if energy < 0.0 or energy > 1.0:
        return False, f"target_energy must be between 0.0 and 1.0, but got {energy}."

    # All checks passed
    return True, "User preferences are valid."


def assess_recommendation_reliability(user_prefs: Dict, recommendations: List) -> Dict[str, str]:
    """
    Rate how reliable a set of recommendations is, based on the top score.

    `recommendations` is the list returned by recommend_songs(), where each
    item is a tuple: (song_dict, score, explanation). The list is already
    sorted from highest to lowest score.

    Returns a dictionary with:
      - "level":   "High", "Medium", or "Low"
      - "message": a short explanation
    """
    # No recommendations at all means we can't trust the result
    if not recommendations:
        return {
            "level": "Low",
            "message": "No recommendations were found, so reliability is low.",
        }

    # Grab the score of the top recommendation (2nd item in the tuple).
    # We use max() just in case the list was not sorted.
    top_score = max(score for _song, score, _explanation in recommendations)

    # Apply the simple threshold rules
    if top_score >= HIGH_RELIABILITY_THRESHOLD:
        level = "High"
        message = (
            f"Top score is {top_score:.2f}. The best match fits your genre, "
            "mood, and energy well."
        )
    elif top_score >= MEDIUM_RELIABILITY_THRESHOLD:
        level = "Medium"
        message = (
            f"Top score is {top_score:.2f}. The best match fits some of your "
            "preferences, but not all of them."
        )
    else:
        level = "Low"
        genre = user_prefs.get("favorite_genre", "your genre")
        message = (
            f"Top score is {top_score:.2f}. No song strongly matched your "
            f"preferences (the catalog may have few '{genre}' songs)."
        )

    return {"level": level, "message": message}
