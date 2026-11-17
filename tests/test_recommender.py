import pytest

from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def make_song_dict(id, title, genre, mood, energy) -> dict:
    """Builds a song dictionary like the ones load_songs() returns."""
    return {
        "id": id,
        "title": title,
        "artist": "Test Artist",
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "tempo_bpm": 100,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.5,
    }


POP_HAPPY_USER = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
}


def test_score_song_full_match_gets_maximum_score():
    song = make_song_dict(1, "Perfect Match", "pop", "happy", 0.80)

    score, reasons = score_song(POP_HAPPY_USER, song)

    assert score == pytest.approx(4.0)
    assert any("genre match" in reason for reason in reasons)
    assert any("mood match" in reason for reason in reasons)
    assert any("energy similarity" in reason for reason in reasons)


def test_score_song_energy_only_match():
    song = make_song_dict(1, "Energy Only", "metal", "angry", 0.80)

    score, reasons = score_song(POP_HAPPY_USER, song)

    assert score == pytest.approx(1.0)
    assert not any("genre match" in reason for reason in reasons)
    assert not any("mood match" in reason for reason in reasons)


def test_recommend_songs_returns_highest_score_first():
    # Songs are listed from worst match to best match on purpose
    songs = [
        make_song_dict(1, "No Match", "classical", "peaceful", 0.10),
        make_song_dict(2, "Mood Match", "rock", "happy", 0.80),
        make_song_dict(3, "Genre Match", "pop", "sad", 0.80),
        make_song_dict(4, "Perfect Match", "pop", "happy", 0.80),
    ]

    results = recommend_songs(POP_HAPPY_USER, songs, k=4)
    titles = [song["title"] for song, score, explanation in results]

    assert titles == ["Perfect Match", "Genre Match", "Mood Match", "No Match"]
    assert results[0][1] == pytest.approx(4.0)


def test_recommender_ranks_songs_instead_of_keeping_original_order():
    weaker_song = Song(
        id=1,
        title="Weaker Song",
        artist="Test Artist",
        genre="lofi",
        mood="chill",
        energy=0.30,
        tempo_bpm=75,
        valence=0.5,
        danceability=0.5,
        acousticness=0.8,
    )
    best_song = Song(
        id=2,
        title="Best Song",
        artist="Test Artist",
        genre="pop",
        mood="happy",
        energy=0.80,
        tempo_bpm=120,
        valence=0.9,
        danceability=0.8,
        acousticness=0.2,
    )
    # The weaker song comes first in the list on purpose
    rec = Recommender([weaker_song, best_song])
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.80,
        likes_acoustic=False,
    )

    results = rec.recommend(user, k=2)

    assert results[0] is best_song
    assert results[1] is weaker_song
