"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender with
multiple scoring modes and diversity-aware ranking.
"""
from pathlib import Path
import textwrap

from tabulate import tabulate

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


PROFILES = [
    {
        "name": "Genre-First: High-Energy Pop",
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
    {
        "name": "Mood-First: Chill Lofi",
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
    {
        "name": "Energy-Focused: Deep Intense Rock",
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
]


def _fallback_table(rows: list[list[str]], headers: list[str]) -> str:
    table = [headers] + rows
    widths = [max(len(str(row[col])) for row in table) for col in range(len(headers))]

    def _format_row(row: list[str]) -> str:
        return "| " + " | ".join(str(value).ljust(widths[idx]) for idx, value in enumerate(row)) + " |"

    divider = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    output = [divider, _format_row(headers), divider]
    for row in rows:
        output.append(_format_row(row))
    output.append(divider)
    return "\n".join(output)


def format_recommendations_table(recommendations: list[tuple[dict, float, str]]) -> str:
    rows: list[list[str]] = []
    for idx, (song, score, _explanation) in enumerate(recommendations, start=1):
        rows.append(
            [
                str(idx),
                song["title"],
                song["artist"] or "Unknown Artist",
                song["genre"],
                f"{score:.2f}",
            ]
        )

    headers = ["Rank", "Title", "Artist", "Genre", "Score"]
    if tabulate is not None:
        return tabulate(rows, headers=headers, tablefmt="grid")
    return _fallback_table(rows, headers)


def _compact_reasons(explanation: str, max_items: int = 3) -> str:
    reasons = [part.strip() for part in explanation.split(";") if part.strip()]
    reasons = [r for r in reasons if not r.startswith("mode:")]
    if not reasons:
        return "No strong feature matches"

    selected = reasons[:max_items]
    if len(reasons) > max_items:
        selected.append("(+more)")
    return selected


def print_recommendations(profile: dict, songs: list[dict]) -> None:
    recommendations = recommend_songs(
        profile["prefs"],
        songs,
        k=5,
        mode=profile["mode"],
        artist_penalty=profile["artist_penalty"],
        genre_penalty=profile["genre_penalty"],
    )

    print(f"\n=== {profile['name']} ===")
    print(f"Mode: {profile['mode']}")
    print(
        "Diversity penalties: "
        f"artist={profile['artist_penalty']}, genre={profile['genre_penalty']}"
    )
    print("Top recommendations:\n")
    print(format_recommendations_table(recommendations))
    print("\nWhy these songs were picked:")
    for idx, (song, _score, explanation) in enumerate(recommendations, start=1):
        compact_reasons = _compact_reasons(explanation)
        print(f"{idx}. {song['title']}")
        for reason in compact_reasons:
            wrapped = textwrap.wrap(reason, width=95)
            if wrapped:
                print(f"   - {wrapped[0]}")
                for line in wrapped[1:]:
                    print(f"     {line}")
    print()


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    songs_path = project_root / "data" / "songs.csv"
    songs = load_songs(str(songs_path))
    for profile in PROFILES:
        print_recommendations(profile, songs)


if __name__ == "__main__":
    main()
