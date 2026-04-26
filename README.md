# 🎵 Music Recommender Simulation

## Project Summary

In this project I'm building a small music recommender system

This version builds a transparent content-based music recommender that scores each song against a user profile and prints the top matches with explanations. I also ran the recommender on three normal profiles and two adversarial edge-case profiles to see how the scoring logic behaves when preferences conflict.

---

## How The System Works

Real-world recommender systems usually combine many signals (what users click, skip, finish, and replay) to estimate what they may enjoy next, then rank candidate items into a final top list. This project implements a transparent, content-based version of that idea: each song is compared with a user profile, scored with weighted rules, and then reranked with diversity penalties before producing the final recommendations.

The architecture has four practical stages:

1. **Input stage:** Load songs from `data/songs.csv` and collect profile preferences from preset profiles (CLI) or sidebar controls (Streamlit).
2. **Scoring stage:** Compute a numeric score per song using weighted feature matching.
3. **Reranking stage:** Apply artist and genre penalties to reduce repetition in the top list.
4. **Presentation stage:** Show a ranked table and short explanation bullets for why each song was selected.

Features used by `Song` include both core and advanced attributes:

- `id`, `title`, `artist`
- `genre`, `mood`
- `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- `popularity`, `release_year`, `mood_tags`, `instrumentalness`, `speechiness`, `liveness`

Features used by `UserProfile` include mode + preference targets:

- `genre`, `mood`, `energy`, `likes_acoustic`
- `preferred_decade`, `target_popularity`, `preferred_mood_tags`
- `target_instrumentalness`, `target_speechiness`, `target_liveness`
- ranking `mode` (`genre_first`, `mood_first`, `energy_focused`)
- `artist_penalty` and `genre_penalty` for diversity-aware reranking

### Algorithm Recipe

1. Read user preferences and select a ranking mode (`genre_first`, `mood_first`, or `energy_focused`).
2. Loop through songs and compute base score components for genre, mood, energy closeness, and acoustic preference.
3. Add advanced feature points from decade, popularity, mood-tag overlap, instrumentalness, speechiness, and liveness closeness.
4. Build a candidate pool with `base_score + reasons` for every song.
5. Select top `K` songs iteratively using adjusted score = `base_score - diversity_penalty`, where the penalty increases when the same artist or genre repeats.
6. Return the ranked songs and explanation strings, then render them as a compact table plus top reason bullets.

### Expected Biases and Limitations

This system might over-prioritize genre, ignoring great songs that better match the user's mood or energy. It may also under-represent songs that are outside the dominant patterns in the small CSV file, since the recommender can only choose from the data it has. Because it uses simple feature matching, it does not understand lyrics, context, or changing user intent over time.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

4. Run the Streamlit frontend (visual demo):

```bash
streamlit run src/streamlit_app.py
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

### Evaluation Screenshots

I captured the terminal output for each profile and saved it as a screenshot so the ranking behavior is easy to review. I also created a streamlit app to visually see what it would look like

#### High-Energy Pop

![High-Energy Pop recommendation output](screenshots/high_energy_pop.png)

#### Chill Lofi

![Chill Lofi recommendation output](screenshots/chill_lofi.png)

#### Deep Intense Rock

![Deep Intense Rock recommendation output](screenshots/deep_intense_rock.png)

#### System Eval: Conflicting Acoustic EDM

![Conflicting Acoustic EDM recommendation output](screenshots/system_eval_conflicting_acoustic_edm.png)

#### System Eval: Boundary Extremist

![Boundary Extremist recommendation output](screenshots/system_eval_boundary_extremist.png)

---

## Loom Walkthrough

Loom video (silent walkthrough): [https://www.loom.com/share/6b36843aa03f45f29b0bdea14923fcd2](https://www.loom.com/share/6b36843aa03f45f29b0bdea14923fcd2)

This walkthrough shows the recommender running end-to-end in the Streamlit frontend with three different input profiles. For each profile, the video shows:

1. Input settings (mode, preference targets, and diversity penalties)
2. Top recommendation table output
3. Explanation bullets showing why songs were selected

### Demo Flow Used in Video

1. Profile A: Genre-First High-Energy Pop
2. Profile B: Mood-First Chill Lofi
3. Profile C: Energy-Focused Deep Intense Rock

---

## Limitations and Risks

This recommender is intentionally simple and transparent, which makes it useful for learning, but it still has important limitations.

- Small and synthetic dataset: The catalog is only 18 songs, so recommendations are constrained by limited genre coverage and may not generalize to real listening behavior.

- Content-only matching: The system uses song attributes and fixed profile preferences, but does not learn from real user interaction history such as skips, repeats, or session context. (something that Spotify/Apple Music/Youtube Music has)

- Feature bias risk: Strong weights on energy, mood, or genre can dominate rankings and create repetitive results if not carefully tuned.

- Partial diversity control: Artist and genre penalties reduce repetition, but they do not guarantee full fairness across all underrepresented styles.

- No semantic understanding: The model does not interpret lyrics, culture, language, or meaning, so two songs with similar numeric features may still feel very different to listeners.

Mitigation ideas used in this project include running multiple profile tests, exposing recommendation reasons for transparency, and applying diversity penalties. Additional mitigation would require a larger dataset, richer user feedback signals, and more systematic fairness evaluation.

---

## Reflection

Building this project helped me understand that recommenders are not just about writing a scoring formula; they are about making clear design choices and then validating the outcomes against real user scenarios. 

I learned how small weight changes can significantly shift rankings, how feature selection can introduce unintended bias, and why transparency matters when presenting AI outputs. 

By testing multiple profiles, adding explanation bullets, and introducing diversity penalties, I saw how an AI engineer has to balance different outputs at the same time. 

This project reflects my approach to AI engineering: build practical systems end-to-end, explain how they work, and iterate responsibly based on observed behavior.

See the full model card here: [**Model Card**](model_card.md)