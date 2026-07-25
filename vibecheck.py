def get_mood():
    """
    Prompts the user to enter their current mood.
    Valid options: happy, sad, focused, energized, anxious, calm
    Reprompts on invalid or empty input.
    Returns: the validated mood as a lowercase string.
    """
    valid_moods = ["happy", "sad", "focused", "energized", "anxious", "calm"]
    while True:
        print(f"Valid moods: {', '.join(valid_moods)}")
        mood = input("How are you feeling? ").strip().lower()
        if mood in valid_moods:
            return mood
        print(f"'{mood}' is not a valid mood. Please try again.\n")
def get_energy():
    """
    Prompts the user to enter their energy level.
    Valid options: low, medium, high
    Reprompts on invalid or empty input.
    Returns: the validated energy level as a lowercase string.
    """
    valid_energy = ["low", "medium", "high"]
    while True:
        print(f"Valid energy levels: {', '.join(valid_energy)}")
        energy = input("What's your energy level? ").strip().lower()
        if energy in valid_energy:
            return energy
        print(f"'{energy}' is not a valid energy level. Please try again.\n")
def load_recommendations(filename):
    """
    Reads the recommendations file and builds a lookup dictionary.
    File format per line: mood|energy|genre|vibe|artist1,artist2,artist3
    Returns: a dictionary structured like:
    {
        "happy": {
            "high": {"genre": ..., "vibe": ..., "artists": [...]},
            "medium": {...},
            "low": {...}
        },
        "sad": {...},
        ...
    }
    """
    recommendations = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                mood, energy, genre, vibe, artists_string = line.split("|")
                artists = artists_string.split(",")
                if mood not in recommendations:
                    recommendations[mood] = {}
                recommendations[mood][energy] = {
                    "genre": genre,
                    "vibe": vibe,
                    "artists": artists,
                }
    except FileNotFoundError:
        print(f"Could not find recommendations file: {filename}")
    return recommendations