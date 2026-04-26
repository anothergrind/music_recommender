from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


PRESET_PROFILES = {
    "Genre-First: High-Energy Pop": {
        "mode": "genre_first",
        "artist_penalty": 0.6,
        "genre_penalty": 0.5,
        "prefs": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "likes_acoustic": False,
            "preferred_decade": 2020,
            "target_popularity": 82,
            "preferred_mood_tags": ["uplifting", "energetic", "feel-good"],
            "target_instrumentalness": 0.15,
            "target_speechiness": 0.06,
            "target_liveness": 0.22,
        },
    },
    "Mood-First: Chill Lofi": {
        "mode": "mood_first",
        "artist_penalty": 0.7,
        "genre_penalty": 0.4,
        "prefs": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
            "preferred_decade": 2020,
            "target_popularity": 68,
            "preferred_mood_tags": ["chill", "study", "focused", "calming"],
            "target_instrumentalness": 0.88,
            "target_speechiness": 0.05,
            "target_liveness": 0.10,
        },
    },
    "Energy-Focused: Deep Intense Rock": {
        "mode": "energy_focused",
        "artist_penalty": 0.8,
        "genre_penalty": 0.4,
        "prefs": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
            "likes_acoustic": False,
            "preferred_decade": 2000,
            "target_popularity": 62,
            "preferred_mood_tags": ["intense", "powerful", "driving", "aggressive"],
            "target_instrumentalness": 0.2,
            "target_speechiness": 0.12,
            "target_liveness": 0.30,
        },
    },
}


def _reason_bullets(explanation: str, max_items: int = 3) -> list[str]:
    reasons = [part.strip() for part in explanation.split(";") if part.strip()]
    reasons = [r for r in reasons if not r.startswith("mode:")]
    if not reasons:
        return ["No strong feature matches"]
    return reasons[:max_items]


def _build_recommendation_table(recommendations: list[tuple[dict, float, str]]) -> pd.DataFrame:
    rows = []
    for idx, (song, score, _explanation) in enumerate(recommendations, start=1):
        rows.append(
            {
                "Rank": idx,
                "Title": song["title"],
                "Artist": song["artist"] or "Unknown Artist",
                "Genre": song["genre"],
                "Score": round(score, 2),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")
    st.title("🎵 Music Recommender Frontend")
    st.caption("Interactive Streamlit UI for your content-based recommender")

    project_root = Path(__file__).resolve().parents[1]
    songs_path = project_root / "data" / "songs.csv"
    songs = load_songs(str(songs_path))

    st.sidebar.header("Profile Setup")
    profile_choice = st.sidebar.selectbox(
        "Choose a profile",
        ["Custom"] + list(PRESET_PROFILES.keys()),
        index=1,
    )

    if profile_choice == "Custom":
        selected = {
            "mode": "genre_first",
            "artist_penalty": 0.6,
            "genre_penalty": 0.4,
            "prefs": {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.7,
                "likes_acoustic": False,
                "preferred_decade": 2020,
                "target_popularity": 70,
                "preferred_mood_tags": ["uplifting", "energetic"],
                "target_instrumentalness": 0.3,
                "target_speechiness": 0.1,
                "target_liveness": 0.2,
            },
        }
    else:
        selected = PRESET_PROFILES[profile_choice]

    mode = st.sidebar.selectbox("Ranking mode", ["genre_first", "mood_first", "energy_focused"], index=["genre_first", "mood_first", "energy_focused"].index(selected["mode"]))
    genre = st.sidebar.text_input("Favorite genre", selected["prefs"]["genre"])
    mood = st.sidebar.text_input("Favorite mood", selected["prefs"]["mood"])
    energy = st.sidebar.slider("Target energy", 0.0, 1.0, float(selected["prefs"]["energy"]), 0.01)
    likes_acoustic = st.sidebar.checkbox("Likes acoustic songs", bool(selected["prefs"]["likes_acoustic"]))

    st.sidebar.subheader("Advanced targets")
    preferred_decade = st.sidebar.selectbox("Preferred decade", [1990, 2000, 2010, 2020], index=[1990, 2000, 2010, 2020].index(int(selected["prefs"]["preferred_decade"])))
    target_popularity = st.sidebar.slider("Target popularity", 0, 100, int(selected["prefs"]["target_popularity"]))
    mood_tags_raw = st.sidebar.text_input("Mood tags (comma-separated)", ", ".join(selected["prefs"]["preferred_mood_tags"]))
    target_instrumentalness = st.sidebar.slider("Target instrumentalness", 0.0, 1.0, float(selected["prefs"]["target_instrumentalness"]), 0.01)
    target_speechiness = st.sidebar.slider("Target speechiness", 0.0, 1.0, float(selected["prefs"]["target_speechiness"]), 0.01)
    target_liveness = st.sidebar.slider("Target liveness", 0.0, 1.0, float(selected["prefs"]["target_liveness"]), 0.01)

    st.sidebar.subheader("Diversity")
    artist_penalty = st.sidebar.slider("Artist penalty", 0.0, 1.5, float(selected["artist_penalty"]), 0.05)
    genre_penalty = st.sidebar.slider("Genre penalty", 0.0, 1.5, float(selected["genre_penalty"]), 0.05)
    top_k = st.sidebar.slider("Top K", 3, 10, 5)

    user_prefs = {
        "genre": genre.strip(),
        "mood": mood.strip(),
        "energy": float(energy),
        "likes_acoustic": bool(likes_acoustic),
        "preferred_decade": int(preferred_decade),
        "target_popularity": int(target_popularity),
        "preferred_mood_tags": [tag.strip() for tag in mood_tags_raw.split(",") if tag.strip()],
        "target_instrumentalness": float(target_instrumentalness),
        "target_speechiness": float(target_speechiness),
        "target_liveness": float(target_liveness),
    }

    recommendations = recommend_songs(
        user_prefs,
        songs,
        k=top_k,
        mode=mode,
        artist_penalty=artist_penalty,
        genre_penalty=genre_penalty,
    )

    st.subheader("Top Recommendations")
    st.dataframe(_build_recommendation_table(recommendations), use_container_width=True, hide_index=True)

    st.subheader("Why These Songs")
    for idx, (song, _score, explanation) in enumerate(recommendations, start=1):
        with st.expander(f"{idx}. {song['title']} - {song['artist'] or 'Unknown Artist'}"):
            for reason in _reason_bullets(explanation, max_items=3):
                st.markdown(f"- {reason}")


if __name__ == "__main__":
    main()