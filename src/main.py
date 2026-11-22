"""
Command line runner for the Music Recommender Simulation.
Run from the project root with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs, DEFAULT_WEIGHTS

PROFILES = {
    # Default starter profile
    "Default Pop/Happy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    # Three distinct profiles
    "High-Energy Pop": {"genre": "pop", "mood": "intense", "energy": 0.93},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    # Adversarial / edge cases
    "Conflicting (high energy + sad)": {"genre": "classical", "mood": "sad", "energy": 0.9},
    "Genre not in catalog (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.8},
    "Middle of the road": {"genre": "jazz", "mood": "relaxed", "energy": 0.5},
}


def show(title: str, user_prefs: dict, songs: list, k: int = 5, weights=None) -> None:
    """Print one profile's top-k recommendations in a readable layout."""
    print("=" * 64)
    print(f"Profile: {title}")
    print(f"Prefs:   genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print("-" * 64)
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k, weights), 1):
        print(f"{rank}. {song['title']} by {song['artist']}  |  Score: {score:.2f} / 4.00")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for title, prefs in PROFILES.items():
        show(title, prefs, songs)

    # Experiment: Weight Shift (double energy, halve genre)
    shifted = {"genre": DEFAULT_WEIGHTS["genre"] / 2, "mood": DEFAULT_WEIGHTS["mood"],
               "energy": DEFAULT_WEIGHTS["energy"] * 2}
    print("#" * 64)
    print(f"EXPERIMENT: weight shift -> {shifted}")
    print("#" * 64 + "\n")
    for title in ("Default Pop/Happy", "High-Energy Pop", "Chill Lofi"):
        show(title + " (shifted weights)", PROFILES[title], songs, weights=shifted)


if __name__ == "__main__":
    main()
