import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Algorithm Recipe: points available for each rule.
# Max score = 2.0 + 1.0 + 1.0 = 4.0
DEFAULT_WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 1.0}


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


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a Song object by converting both sides to dicts and reusing score_song."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        return score_song(prefs, song.__dict__)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for a user, best first."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song scored the way it did."""
        score, reasons = self._score(user, song)
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float."""
    int_fields = ["id"]
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in int_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict,
               weights: Optional[Dict[str, float]] = None) -> Tuple[float, List[str]]:
    """Score one song against user prefs; return (score, list of human-readable reasons)."""
    w = weights or DEFAULT_WEIGHTS
    score = 0.0
    reasons: List[str] = []

    # Rule 1: genre match is all-or-nothing.
    if song["genre"] == user_prefs.get("genre"):
        score += w["genre"]
        reasons.append(f"genre match: {song['genre']} (+{w['genre']:.1f})")

    # Rule 2: mood match is all-or-nothing.
    if song["mood"] == user_prefs.get("mood"):
        score += w["mood"]
        reasons.append(f"mood match: {song['mood']} (+{w['mood']:.1f})")

    # Rule 3: energy rewards CLOSENESS to the target, not just high or low values.
    # similarity = 1 - |song - target|, so a perfect match gives 1.0 and the
    # furthest possible miss gives 0.0 (energy lives on a 0 to 1 scale).
    if "energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["energy"])
        points = w["energy"] * (1.0 - gap)
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    weights: Optional[Dict[str, float]] = None) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort best-first, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a NEW list and leaves `songs` untouched (list.sort() would
    # reorder in place). Python's sort is stable, so ties keep CSV order.
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
