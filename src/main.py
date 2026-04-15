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

    # --- User Profiles ---

    # Profile 1: Study / Focus — prefers calm, acoustic lofi with low energy
    study_user = {
        "favorite_genre":  "lofi",
        "favorite_mood":   "chill",
        "target_energy":   0.40,
        "likes_acoustic":  True,
        "related_genres":  ["ambient", "classical"],
        "related_moods":   ["focused", "relaxed", "peaceful"],
    }

    # Profile 2: Workout / Hype — wants high-energy, danceable pop/rock
    workout_user = {
        "favorite_genre":  "pop",
        "favorite_mood":   "intense",
        "target_energy":   0.90,
        "likes_acoustic":  False,
        "related_genres":  ["rock", "techno", "metal"],
        "related_moods":   ["energetic", "triumphant", "dark"],
    }

    # Profile 3: Late-Night Drive — moody synthwave with moderate energy
    latenight_user = {
        "favorite_genre":  "synthwave",
        "favorite_mood":   "moody",
        "target_energy":   0.70,
        "likes_acoustic":  False,
        "related_genres":  ["indie pop", "soul", "blues"],
        "related_moods":   ["melancholic", "reflective", "dramatic"],
    }

    user_profiles = [
        ("Study / Focus",      study_user),
        ("Workout / Hype",     workout_user),
        ("Late-Night Drive",   latenight_user),
    ]

    for profile_name, user_prefs in user_profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 50)
        print(f"Profile: {profile_name}")
        print("User Preferences:")
        for key, value in user_prefs.items():
            print(f"  {key}: {value}")
        print("  Top Recommendations")
        print("=" * 50)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']} by {song['artist']} (Score: {score:.2f})")
            print(f"    Why:   {explanation}")
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
