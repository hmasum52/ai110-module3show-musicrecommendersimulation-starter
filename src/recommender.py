from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    related_genres: List[str] = field(default_factory=list)
    related_moods: List[str] = field(default_factory=list)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, score_song(asdict(user), asdict(song))[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(asdict(user), asdict(song))
        explanation = ", ".join(reasons) if reasons else "no strong match"
        return f"Score {score:.2f}: {explanation}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons: List[str] = []

    # --- Genre score (weight 0.44) ---
    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre", ""))
    related_genres: List[str] = user_prefs.get("related_genres", [])
    if song["genre"] == favorite_genre:
        genre_score = 1.0
        reasons.append(f"exact genre match ({song['genre']})")
    elif song["genre"] in related_genres:
        genre_score = 0.5
        reasons.append(f"related genre ({song['genre']})")
    else:
        genre_score = 0.0

    # --- Mood score (weight 0.22) ---
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood", ""))
    related_moods: List[str] = user_prefs.get("related_moods", [])
    if song["mood"] == favorite_mood:
        mood_score = 1.0
        reasons.append(f"exact mood match ({song['mood']})")
    elif song["mood"] in related_moods:
        mood_score = 0.5
        reasons.append(f"related mood ({song['mood']})")
    else:
        mood_score = 0.0

    # --- Energy score (weight 0.22) ---
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy", 0.5))
    energy_score = 1.0 - abs(target_energy - song["energy"])
    reasons.append(f"energy proximity {energy_score:.2f}")

    # --- Acousticness score (weight 0.11) ---
    likes_acoustic: bool = user_prefs.get("likes_acoustic", True)
    acoustic_score = song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"]
    if likes_acoustic:
        reasons.append(f"acousticness {song['acousticness']:.2f}")

    total = (
        genre_score    * 0.22 +
        mood_score     * 0.22 +
        energy_score   * 0.44 +
        acoustic_score * 0.11
    )

    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
