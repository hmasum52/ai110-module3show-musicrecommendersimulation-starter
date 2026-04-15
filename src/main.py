"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    user_prefs = {
        "favorite_genre":  "lofi",
        "favorite_mood":   "chill",
        "target_energy":   0.40,
        "likes_acoustic":  True,
        "related_genres":  ["ambient"],
        "related_moods":   ["focused", "relaxed"],
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    # print user preferences
    print("User Preferences:")
    for key, value in user_prefs.items():
        print(f"  {key}: {value}")
    print("  Top Recommendations")
    print("=" * 50)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar = "#" * int(score * 20)
        print(f"\n#{rank}  {song['title']} by {song['artist']} (Score: {score:.2f})")
        print(f"    Why:   {explanation}")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
