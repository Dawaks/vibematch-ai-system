# VibeMatch AI: Explainable and Reliability-Checked Music Recommender

## Project Summary

VibeMatch AI recommends songs based on a listener's favorite genre, favorite mood, and target energy level. It builds on my earlier Music Recommender Simulation, which used a simple scoring system to rank songs and explain each choice.

The final version wraps that recommender with input validation, a reliability assessment, clear explanations, and automated tests. The goal is a system that doesn't just give recommendations, but also shows why it made them and how confident it should be in them.

---

## Original Project

VibeMatch AI extends my earlier Music Recommender Simulation. The original project recommended songs with a simple content-based scoring system that compared each song's genre, mood, and energy to a user's favorite genre, favorite mood, and target energy. It ranked the songs by score and explained why each one was recommended.

## What VibeMatch AI Adds

The upgraded system keeps the original scoring logic and adds a reliability layer around it:

- **Input validation** checks user preferences before any recommendations are generated.
- **Recommendation reliability levels** (High, Medium, or Low) show how strongly the top result matches the user.
- **Clearer explanations** describe the score breakdown and what the reliability level means.
- **Automated reliability tests** cover both validation and reliability scoring.
- **An edge-case evaluation profile** tests how the system behaves when the user's preferences are only partly represented in the catalog.

## Architecture Overview

The system architecture is documented in [`diagrams/architecture.mmd`](diagrams/architecture.mmd) as a Mermaid flowchart. The flow works like this:

1. A user profile enters the system through `src/main.py`.
2. `src/reliability.py` validates the input. Invalid profiles are reported and skipped.
3. `src/recommender.py` scores and ranks songs from `data/songs.csv`.
4. An explanation is generated for each recommendation, showing how its score was built.
5. `src/reliability.py` assigns a reliability level based on the top score.
6. `src/main.py` displays the recommendations together with the reliability level and message.
7. Automated tests in `tests/` check the recommender, the input validation, and the reliability logic.

## Reliability and Guardrails

The reliability features live in `src/reliability.py` and are used by `src/main.py`.

**Input validation.** User preferences are validated before recommendations are generated. If a profile fails validation, the system prints the reason and skips that profile instead of producing misleading results. A profile is valid when:

- `favorite_genre` is a non-empty string
- `favorite_mood` is a non-empty string
- `target_energy` is a number between 0.0 and 1.0

**Reliability levels.** After generating recommendations, the system rates their reliability based on the top recommendation's score. The highest possible score is 4.0.

| Level | Top recommendation score |
|---|---|
| High | >= 3.0 |
| Medium | >= 2.0 and < 3.0 |
| Low | < 2.0 (or no recommendations) |

Reliability is an internal system signal. It shows how well the top song matches the user's stated preferences under this scoring system. It does not guarantee that a recommendation is objectively correct or that the user will enjoy it.

## Example Interactions

**Example 1: High-Energy Pop**

```text
Top recommendation:
Sunrise City - Score: 3.98
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

Reliability: High
Top score is 3.98. The best match fits your genre, mood, and energy well.
```

**Example 2: Chill Lofi**

```text
Top recommendation:
Library Rain - Score: 4.00
Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.00)

Reliability: High
Top score is 4.00. The best match fits your genre, mood, and energy well.
```

**Example 3: Edge Case**

```text
Input:
genre=classical
mood=angry
energy=0.95

Top recommendation:
Glass Winter Etude - Score: 2.20
Because: genre match (+2.0), energy similarity (+0.20)

Reliability: Medium
Top score is 2.20. The best match fits some of your preferences, but not all of them.
```

In the edge case, the top song matches the genre but is far from the target energy. The Medium rating signals that the result is only a partial match.

## Reliability Evaluation

| Profile | Top Score | Reliability | Observation |
|---|---|---|---|
| High-Energy Pop | 3.98 | High | Strong match across genre, mood, and energy |
| Chill Lofi | 4.00 | High | Exact or near-exact match across all main preferences |
| Intense Rock | 3.99 | High | Strong match across all main preferences |
| Edge Case | 2.20 | Medium | Only part of the user's preference combination was strongly represented |

## Testing Summary

All 13 automated tests pass (`pytest`):

- **6 tests** in `tests/test_recommender.py` cover the recommender.
- **7 tests** in `tests/test_reliability.py` cover validation and reliability.

Together, the tests cover valid input, invalid input, reliability score thresholds, empty recommendation lists, ranking order, and explanation behavior.

## Design Decisions

- **I kept the original rule-based scoring model.** Every score can be traced back to a few simple rules, which makes the system easy to inspect and explain.
- **I added guardrails around it instead of replacing it.** Rather than switching to a more complex model, I added input validation before recommending and a reliability check afterward. This improves trustworthiness without hiding how the system works.
- **Reliability is based on the top score.** This is simple and easy to audit. However, it is only an internal signal about how well the best match fits the stated preferences, not a guarantee that the user will be satisfied.
- **I kept exact genre and mood matching.** This keeps the logic simple, even though it means related genres such as "pop" and "indie pop" are treated as completely different.

---

## How The System Works

This project uses a simple **content-based recommendation system**. Instead of looking at what other people listen to, it compares a user's preferences directly with the features of each song.

Each song is described using three features:

- **genre** – the style of music (for example, pop or rock)
- **mood** – the feeling of the song (for example, happy or chill)
- **energy** – how intense or active the song feels, on a scale from low to high

The user profile stores a favorite genre, a favorite mood, and a target energy level. The recommender gives every song a score based on how well it matches those preferences.

### Algorithm Recipe

For each song, the score is built like this:

1. **+2.0 points** if the song's genre exactly matches the user's favorite genre.
2. **+1.0 point** if the song's mood exactly matches the user's favorite mood.
3. **Up to +1.0 point** based on how close the song's energy is to the user's target energy. The closer the energy, the more points the song gets.
4. **Rank** all songs from highest score to lowest score, and recommend the songs at the top.

### Limitation

Genre has more influence than mood or energy. Because of this, the system may favor songs in the preferred genre even when another song has a better overall mood or energy match.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .\.venv\Scripts\Activate.ps1   # Windows PowerShell
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the automated tests with:

```bash
python -m pytest
```

Recommender tests live in `tests/test_recommender.py`, and validation and reliability tests live in `tests/test_reliability.py`.

---

## Sample Recommendation Output

The output below comes from running `python -m src.main` with the High-Energy Pop profile (favorite genre: pop, favorite mood: happy, target energy: 0.80):

```text
Loading songs from data/songs.csv...

Top recommendations:

Sunrise City - Score: 3.98
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

Gym Hero - Score: 2.87
Because: genre match (+2.0), energy similarity (+0.87)

Rooftop Lights - Score: 1.96
Because: mood match (+1.0), energy similarity (+0.96)

Night Drive Loop - Score: 0.95
Because: energy similarity (+0.95)

Concrete Crown - Score: 0.91
Because: energy similarity (+0.91)
```

---

## Experiments You Tried

### Experiment: Changing the Scoring Weights

I tested what happens when genre counts for less and energy counts for more. I ran the same three user profiles (High-Energy Pop, Chill Lofi, and Intense Rock) with both sets of weights.

| Feature | Original scoring | Experimental scoring |
|---|---|---|
| Genre match | +2.0 | +1.0 |
| Mood match | +1.0 | +1.0 |
| Energy similarity | up to +1.0 | up to +2.0 |

**What happened:**

- **High-Energy Pop:** Rooftop Lights moved above Gym Hero. Mood and energy became more influential and genre became less dominant, so a happy song with close energy beat a pop song with the wrong mood.
- **Chill Lofi:** The ranking stayed mostly the same, because the strongest songs already matched genre, mood, and energy well.
- **Intense Rock:** The ranking also stayed mostly the same, because Storm Runner was already a strong match across all three features.

**What I learned:**

- Increasing the energy weight made the system more sensitive to energy similarity.
- This reduced genre dominance, but it also allowed songs with no genre or mood match to score relatively high when their energy was close to the target.

**Conclusion:** I restored the original weights because they provide a simpler and more balanced baseline for this project.

---

## Limitations and Risks

- **Small catalog.** The song catalog is small, so some combinations of preferences have few or no strong matches.
- **Exact matching.** Genre and mood must match exactly, so closely related labels (such as "pop" and "indie pop") get no credit for being similar.
- **Genre has strong influence.** A genre match is worth as much as a mood match and a perfect energy match combined, so genre can strongly affect the ranking.
- **Reliability depends only on the top score.** It doesn't consider how good the rest of the list is or how varied it is.
- **Limited signals.** The system does not use listening history, lyrics, language, artist preferences, or collaborative filtering (what similar listeners enjoy).
- **High reliability is not a promise.** A High rating means the top song fits the stated preferences well under this scoring system. It does not guarantee the user will enjoy the song.

---

## Reflection

This project showed me how much a recommender's behavior depends on the choices behind it. The weights in the scoring rule and the way songs are labeled in the data shape every result. A small change, like making genre worth more than energy, can change which songs a user sees, even when the user's preferences stay the same.

Adding reliability checks made me think more carefully about confidence. A recommender will always return something, even when nothing in the catalog is a good fit. I learned that a trustworthy system should be able to tell the difference and warn the user when a result is only a partial match, instead of presenting every recommendation with the same certainty. My more detailed responsible-AI reflection is in the [Model Card](model_card.md).
