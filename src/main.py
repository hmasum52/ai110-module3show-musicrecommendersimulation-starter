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

    # --- Adversarial / Edge-Case Profiles ---

    # EDGE 1: "Impossible Unicorn"
    # genre + mood don't exist in the catalog at all.
    # Expected flaw: genre (0.44) and mood (0.22) weights are completely wasted —
    # 66% of the scoring formula contributes nothing. Rankings collapse to
    # energy proximity + acousticness only (max possible score = 0.33).
    impossible_user = {
        "favorite_genre":  "reggae",          # not in catalog
        "favorite_mood":   "sad",             # not in catalog
        "target_energy":   0.60,
        "likes_acoustic":  False,
        "related_genres":  [],
        "related_moods":   [],
    }

    # EDGE 2: "Loud Silence"
    # Wants a peaceful mood but demands extreme energy (0.97).
    # Velvet Cathedral is the only peaceful song — energy 0.18 — so it gets
    # crushed by the energy penalty. Loud, non-peaceful songs bubble up instead.
    # Expected flaw: the "right" song for mood ends up near the bottom.
    loud_silence_user = {
        "favorite_genre":  "classical",
        "favorite_mood":   "peaceful",
        "target_energy":   0.97,              # fights directly against peaceful songs
        "likes_acoustic":  True,
        "related_genres":  [],
        "related_moods":   [],
    }

    # EDGE 3: "Acoustic Betrayal"
    # Likes genres that are inherently acoustic (folk, country, blues, lofi)
    # but explicitly dislikes acoustic sound. Genre matches reward the very
    # songs that the acoustic penalty punishes — they fight each other.
    # Expected flaw: no song can score well; high-energy electric songs may
    # surface despite being a terrible genre/mood fit.
    acoustic_betrayal_user = {
        "favorite_genre":  "folk",
        "favorite_mood":   "wistful",
        "target_energy":   0.41,
        "likes_acoustic":  False,             # penalizes folk/country/blues/lofi
        "related_genres":  ["country", "blues", "lofi"],
        "related_moods":   ["reflective", "melancholic", "chill"],
    }

    # EDGE 4: "Duplicate Trap"
    # favorite_genre/mood also appear inside related_genres/related_moods.
    # Because score_song uses elif, the related list is never checked when
    # there's an exact match — the duplicates are silently ignored.
    # Confirms the elif short-circuit doesn't accidentally double-count.
    duplicate_trap_user = {
        "favorite_genre":  "lofi",
        "favorite_mood":   "chill",
        "target_energy":   0.40,
        "likes_acoustic":  True,
        "related_genres":  ["lofi", "ambient"],   # "lofi" is a duplicate
        "related_moods":   ["chill", "focused"],  # "chill" is a duplicate
    }

    # EDGE 5: "Reverse-Engineered Max Score"
    # Preferences are crafted to give Velvet Cathedral (id=11) a near-perfect
    # score (≈0.98). Tests whether the scorer can be gamed to surface one
    # specific song and whether other songs can even compete.
    max_score_user = {
        "favorite_genre":  "classical",       # exact match → 0.44
        "favorite_mood":   "peaceful",        # exact match → 0.22
        "target_energy":   0.18,              # Velvet Cathedral's exact energy → 0.22
        "likes_acoustic":  True,              # acousticness 0.95 → ~0.10
        "related_genres":  [],
        "related_moods":   [],
    }

    user_profiles = [
        ("Study / Focus",           study_user),
        ("Workout / Hype",          workout_user),
        ("Late-Night Drive",        latenight_user),
        ("[EDGE] Impossible Unicorn",       impossible_user),
        ("[EDGE] Loud Silence",             loud_silence_user),
        ("[EDGE] Acoustic Betrayal",        acoustic_betrayal_user),
        ("[EDGE] Duplicate Trap",           duplicate_trap_user),
        ("[EDGE] Reverse-Engineered Max",   max_score_user),
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
