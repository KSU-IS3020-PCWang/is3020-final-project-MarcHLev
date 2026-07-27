import csv
import os
from datetime import datetime


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

                try:
                    mood, energy, genre, vibe, artists_string = line.split("|")
                except ValueError:
                    print(f"Skipping malformed line: {line}")
                    continue

                artists = [artist.strip() for artist in artists_string.split(",")]

                # First time seeing this mood — need to initialize its inner
                # dict before we can assign an energy-level key into it.
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


def get_recommendation(mood, energy, data):
    """
    Looks up the recommendation for a given mood/energy combo.

    Args:
        mood: validated mood string (e.g. "happy")
        energy: validated energy string (e.g. "high")
        data: the nested dict returned by load_recommendations()

    Returns:
        the recommendation dict {"genre": ..., "vibe": ..., "artists": [...]}
        if the combo exists, otherwise None.

        Design decision: returning None (rather than crashing or raising)
        lets display_recommendation() decide how to communicate a missing
        combo to the user, e.g. print a friendly "no recommendation found
        for that combo, try a different mood/energy pairing" message.
    """
    if mood in data and energy in data[mood]:
        return data[mood][energy]

    return None


def display_recommendation(result):
    """
    Displays a recommendation to the user.

    Args:
        result: the dict returned by get_recommendation() — either
                {"genre": ..., "vibe": ..., "artists": [...]} or None.
    """
    if result is None:
        print("No recommendation found for that mood/energy combination — "
              "try a different pairing.")
        return

    print(f"\nGenre: {result['genre']}")
    print(f"Vibe: {result['vibe']}")
    print(f"Artists: {', '.join(result['artists'])}")


def log_session(mood, energy, genre, filename="history.csv"):
    """
    Appends one row to history.csv recording this recommendation session.

    Args:
        mood: validated mood string
        energy: validated energy string
        genre: the genre from the matched recommendation
        filename: path to the history CSV (defaults to history.csv)

    Writes a header row (date, mood, energy, genre) the first time the
    file is created, then appends timestamp + mood + energy + genre
    on every call.
    """
    # This check has to happen BEFORE opening the file in "a" mode —
    # opening in append mode creates the file if it's missing, so
    # checking existence after opening would always say True.
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["date", "mood", "energy", "genre"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, mood, energy, genre])


def show_history(filename="history.csv"):
    """
    Reads history.csv and prints past recommendation sessions.

    Args:
        filename: path to the history CSV (defaults to history.csv)
    """
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            if not rows:
                print("No sessions logged yet.")
                return

            for row in rows:
                if None in (row['date'], row['mood'], row['energy'], row['genre']):
                    print("Skipping a corrupted history row")
                    continue

                print(f"On {row['date']}: felt {row['mood']}, "
                      f"energy {row['energy']} \u2192 {row['genre']}")
    except FileNotFoundError:
        print("No sessions logged yet.")


def main():
    """
    Ties all the pieces together: loads recommendation data, runs the
    mood/energy prompt loop, displays + logs recommendations, and lets
    the user check their history or run another session.
    """
    data = load_recommendations("data/recommendations.txt")

    while True:
        try:
            mood = get_mood()
            energy = get_energy()
            result = get_recommendation(mood, energy, data)
            display_recommendation(result)

            # Only log a session and offer to view history if a
            # recommendation was actually found — otherwise there's no
            # real genre to record, and asking to view history right
            # after a "not found" message feels like a non sequitur.
            if result is not None:
                log_session(mood, energy, result["genre"])

                view_history = input("\nView past sessions? (y/n) ").strip().lower()
                if view_history == "y":
                    show_history()

            again = input("\nCheck another mood? (y/n) ").strip().lower()
            if again != "y":
                print("Take care!")
                break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()