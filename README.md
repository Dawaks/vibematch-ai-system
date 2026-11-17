# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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
   .venv\Scripts\activate         # Windows
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

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

The output below comes from running `python -m src.main` with the starter user profile (favorite genre: pop, favorite mood: happy, target energy: 0.80):

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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
