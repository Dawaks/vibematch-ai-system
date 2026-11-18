"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
from .reliability import validate_user_preferences, assess_recommendation_reliability


# User profiles used to evaluate the recommender
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
    },
    "Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
    },
    "Edge Case": {
        "favorite_genre": "classical",
        "favorite_mood": "angry",
        "target_energy": 0.95,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        print()
        print("=" * 60)
        print(f"Profile: {profile_name}")

        # Step 1: Validate the profile BEFORE recommending anything
        is_valid, validation_message = validate_user_preferences(user_prefs)
        if not is_valid:
            print("Input validation failed")
            print(f"Reason: {validation_message}")
            print("=" * 60)
            continue  # Skip this profile and move on to the next one

        print(
            f"(genre={user_prefs['favorite_genre']}, "
            f"mood={user_prefs['favorite_mood']}, "
            f"energy={user_prefs['target_energy']:.2f})"
        )
        print("=" * 60)

        # Step 2: Generate and print the top 5 recommendations
        recommendations = recommend_songs(user_prefs, songs, k=5)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} - Score: {score:.2f}")
            print(f"   Because: {explanation}")

        # Step 3: Check how reliable these recommendations are
        reliability = assess_recommendation_reliability(user_prefs, recommendations)
        print()
        print(f"Reliability: {reliability['level']}")
        print(f"   {reliability['message']}")


if __name__ == "__main__":
    main()
