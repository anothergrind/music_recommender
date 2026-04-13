"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for idx, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [part.strip() for part in explanation.split(";") if part.strip()]

        print(f"{idx}. {song['title']}")
        print(f"   Final score: {score:.2f}")
        print("   Reasons:")
        if reasons:
            for reason in reasons:
                print(f"   - {reason}")
        else:
            print("   - No specific reasons provided")
        print()


if __name__ == "__main__":
    main()
