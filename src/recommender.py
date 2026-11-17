import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Turn the UserProfile into the dictionary format score_song() expects
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
        }

        # Score every Song using the same rules as score_song()
        scored_songs = []
        for song in self.songs:
            score, reasons = score_song(user_prefs, asdict(song))
            scored_songs.append((song, score))

        # Sort from highest score to lowest score
        scored_songs.sort(key=lambda item: item[1], reverse=True)

        # Return only the top k Song objects
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # Turn the UserProfile into the dictionary format score_song() expects
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
        }

        score, reasons = score_song(user_prefs, asdict(song))

        return (
            f"'{song.title}' (genre: {song.genre}, mood: {song.mood}, "
            f"energy: {song.energy:.2f}) scored {score:.2f} for your profile "
            f"(genre: {user.favorite_genre}, mood: {user.favorite_mood}, "
            f"energy: {user.target_energy:.2f}). "
            f"Reasons: {', '.join(reasons)}."
        )

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # Rule 1: +2.0 points for an exact genre match
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Rule 2: +1.0 point for an exact mood match
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Rule 3: up to +1.0 point for energy similarity (never below 0)
    energy_points = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    energy_points = max(0.0, energy_points)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    results = []

    # Score every song and turn its reasons into one readable sentence
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        results.append((song, score, explanation))

    # Sort from highest score to lowest score
    results.sort(key=lambda result: result[1], reverse=True)

    # Return only the top k results
    return results[:k]
