def get_mood():
    """
    Prompts the user to enter their current mood.
    Valid options: happy, sad, focused, energized, anxious, calm
    Reprompts on invalid or empty input.
    Returns: the validated mood as a lowercase string.
    """
    valid_moods = ["happy", "sad", "focused", "energized", "anxious", "calm"]
    # TODO: loop until the user enters a valid mood
    #   - print the valid options so they know what to type
    #   - get input, strip whitespace, convert to lowercase
    #   - check if it's in valid_moods
    #   - if not valid, print an error message and loop again
    #   - if valid, return it
    pass
def get_energy():
    """
    Prompts the user to enter their energy level.
    Valid options: low, medium, high
    Reprompts on invalid or empty input.
    Returns: the validated energy level as a lowercase string.
    """
    valid_energy = ["low", "medium", "high"]
    # TODO: same validation pattern as get_mood()
    pass
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
    # TODO:
    #   - open the file for reading
    #   - loop through each line
    #   - strip whitespace, skip empty lines
    #   - split the line on "|" to get: mood, energy, genre, vibe, artists_string
    #   - split artists_string on "," to get a list of 3 artists
    #   - build the nested dictionary structure shown above
    #     (hint: if mood isn't already a key in the dict, add it as an empty dict first)
    #   - return the completed dictionary
    pass