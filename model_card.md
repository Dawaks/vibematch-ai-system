# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch suggests songs from a small catalog based on one user's taste profile. The user gives a favorite genre, a favorite mood, and a target energy level, and the system returns the top 5 matching songs with a short explanation for each.

The model assumes that a user's taste can be described by these three preferences and that they want songs close to them. It is built for **classroom exploration** of how recommender systems work, not for real users.

---

## 3. How the Model Works

This recommender is **content-based**. It does not look at what other listeners like. Instead, it compares each song directly with one user's tastes: their **favorite genre**, **favorite mood**, and **target energy** level.

Every song gets a score:

- **+2.0 points** if the song's genre exactly matches the user's favorite genre.
- **+1.0 point** if the song's mood exactly matches the user's favorite mood.
- **Up to +1.0 point** for energy. The closer the song's energy is to the user's target, the more points it gets.

The songs are then ranked from highest score to lowest, and the top songs are recommended. For each recommendation, the system also gives the reasons behind its score (for example, "genre match (+2.0), energy similarity (+0.98)"), so it is easy to see why a song was chosen.

---

## 4. Data

The catalog is a CSV file of **18 fictional songs**. Each song has a genre, mood, energy, tempo, valence, danceability, and acousticness value.

- The starter dataset had 10 songs, mostly pop, lofi, and other calm or upbeat styles.
- I added 8 songs to increase diversity: folk, hip hop, metal, R&B, classical, EDM, country, and reggae, with new moods such as melancholic, angry, romantic, peaceful, euphoric, and nostalgic.
- The catalog now covers 15 genres, energy from 0.15 to 0.97, and tempos from 52 to 176 BPM.

**What is missing:** most genres have only one song, and the data has no lyrics, language, artist popularity, or release year. Tempo, valence, danceability, and acousticness are stored but not used in scoring.

---

## 5. Strengths

- Works well when the catalog contains a song that matches all three preferences. Each test profile got its expected top song (Sunrise City, Library Rain, and Storm Runner) with a score close to the 4.0 maximum.
- Low-energy and high-energy users get clearly different results, so the energy score separates calm and intense music well.
- Every recommendation comes with readable reasons, which makes the results easy to check and understand.

---

## 6. Limitations and Bias

- **Genre dominance:** a genre match is worth twice as much as a mood match, so the system may favor songs in the preferred genre even when another song has a better overall mood or energy match. For the High-Energy Pop profile, Gym Hero (pop, intense) ranked above Rooftop Lights (indie pop, happy).
- **Exact matching only:** "indie pop" gets no credit for "pop", and "metal" gets no credit for "rock", even though these styles are closely related.
- **Small, uneven catalog:** users whose favorite genre has only one song (such as rock) quickly run out of good matches, and lower-ranked results are decided by energy alone.
- **Limited features:** the model ignores lyrics, language, tempo, and other details that shape real musical taste.

---

## 7. Evaluation

I tested three user profiles:

| Profile | Genre | Mood | Target energy | Top result |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.80 | Sunrise City (3.98) |
| Chill Lofi | lofi | chill | 0.35 | Library Rain (4.00) |
| Intense Rock | rock | intense | 0.90 | Storm Runner (3.99) |

I checked whether the top songs matched my expectations and whether the reasons made sense. All three top results matched my intuition.

I also ran a weight experiment, changing genre to +1.0 and energy to up to +2.0. This moved Rooftop Lights above Gym Hero for the pop profile and reduced genre dominance, but it also let songs with no genre or mood match score relatively high. I restored the original weights as a simpler, more balanced baseline. The starter unit tests also pass.

---

## 8. Future Work

- Give partial credit for related genres and moods (for example, "indie pop" and "pop").
- Use more features, such as tempo, valence, or acousticness.
- Add more songs per genre so every type of user has several good matches.
- Improve diversity in the top results so they are not all from the same genre or artist.
- Support users with more than one favorite genre or mood.

---

## 9. Personal Reflection

Building VibeMatch showed me that a recommender is really a set of choices about what matters. Small changes to the scoring weights changed which songs reached the top, even though the data stayed the same. I was surprised by how much the genre weight decided the results, and how an exact-match rule could miss songs a listener would probably enjoy. This made me realize that real music apps are also making design decisions that shape what people hear, and those decisions can favor some tastes over others.
