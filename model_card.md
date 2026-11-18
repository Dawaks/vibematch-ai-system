# 🎧 Model Card: VibeMatch AI

## 1. Model Name

**VibeMatch AI**

VibeMatch AI is an explainable music recommender with built-in input validation and recommendation reliability checks.

---

## 2. Intended Use

VibeMatch AI suggests songs from a small catalog based on a user's favorite genre, favorite mood, and target energy level. It returns the top matching songs, explains why they were selected, and gives the overall recommendation a High, Medium, or Low reliability level.

The system is designed as a classroom and portfolio project to demonstrate how a simple recommender can become more transparent and reliable through guardrails, testing, and clear explanations.

It is not designed to replace a commercial music recommender. It does not use listening history, skips, likes, artist preferences, or information from other listeners.

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

## 6. Limitations, Bias, and Potential Misuse

- **Genre has strong influence:** a genre match is worth twice as much as a mood match, so genre can strongly affect the ranking. For the High-Energy Pop profile, Gym Hero ranked above Rooftop Lights even though Rooftop Lights matched the user's mood and energy more closely.
- **Exact matching only:** "indie pop" receives no genre credit for "pop", and "metal" receives no genre credit for "rock", even though these genres are related.
- **Small and uneven catalog:** some genres have only one song, so users with those preferences quickly run out of strong matches.
- **Limited features:** the recommender does not use listening history, lyrics, language, artist preference, or collaborative filtering.
- **Reliability is simplified:** the High, Medium, and Low rating is based only on the top recommendation's score. It does not measure whether the user will actually enjoy the song.

The system could be misused if someone treated the reliability rating as proof that a recommendation is objectively correct. To reduce this risk, VibeMatch explains that reliability only describes how well the recommendation matches the current scoring rules. It also validates user input before generating recommendations and signals when the strongest match is only partial through a Medium or Low reliability rating.

---

## 7. Evaluation

I evaluated VibeMatch AI using four different profiles:

| Profile | Genre | Mood | Target Energy | Top Result | Reliability |
|---|---|---|---:|---|---|
| High-Energy Pop | pop | happy | 0.80 | Sunrise City (3.98) | High |
| Chill Lofi | lofi | chill | 0.35 | Library Rain (4.00) | High |
| Intense Rock | rock | intense | 0.90 | Storm Runner (3.99) | High |
| Edge Case | classical | angry | 0.95 | Glass Winter Etude (2.20) | Medium |

The first three profiles produced strong matches and High reliability. The edge case was more useful for testing the reliability layer because no song matched the full combination of classical, angry, and high energy. The system returned Glass Winter Etude because it matched the genre, but its low energy made the overall result weaker, so the reliability level dropped to Medium.

That result surprised me because it showed that a recommender will still produce a top result even when the available choices are not especially strong. Adding the reliability layer made that weakness visible instead of presenting every recommendation with the same confidence.

I also ran a controlled scoring experiment where I reduced genre from +2.0 to +1.0 and increased energy from up to +1.0 to up to +2.0. Rooftop Lights then moved above Gym Hero for the High-Energy Pop profile. This showed how strongly feature weights influence the final ranking.

The project currently has **13 passing automated tests**:

- 6 tests for recommendation and explanation behavior
- 7 tests for input validation and reliability behavior

The tests include valid and invalid inputs, recommendation ordering, reliability thresholds, empty recommendation lists, and explanation behavior.

---

## 8. Future Work

- Give partial credit for related genres and moods (for example, "indie pop" and "pop").
- Use more features, such as tempo, valence, or acousticness.
- Add more songs per genre so every type of user has several good matches.
- Improve diversity in the top results so they are not all from the same genre or artist.
- Support users with more than one favorite genre or mood.

---

## 9. Personal Reflection and AI Collaboration

Building VibeMatch AI showed me that a recommender is not just about finding the highest score. The way the data is represented, the weights assigned to each feature, and the rules used to interpret the result all affect what the user sees. I was especially surprised by how much the ranking changed when I adjusted the genre and energy weights.

Adding the reliability layer also changed the way I thought about the system. Before, the recommender always returned a result, even when the available songs were not a strong fit. The edge-case test showed me why it is important for an AI system to communicate uncertainty rather than presenting every answer with the same level of confidence.

I used AI throughout the project to help me break the work into smaller steps, review code, suggest tests, and think through reliability cases. One suggestion I accepted was adding a separate reliability module with input validation and High, Medium, and Low reliability levels. I accepted it because it improved the original recommender without making the system difficult to understand.

One suggestion I did not keep as written was changing the final scoring weights to make energy more important than genre. The experiment produced some interesting results, but it also allowed songs with no genre or mood match to score relatively high. I decided to restore the original weights and document the experiment instead. This helped me see that AI suggestions are useful starting points, but they still need to be tested and judged based on the goals of the system.
