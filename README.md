# IS 3020 Final Project

## Student and Project Information

- Student name: Marc Leveille
- GitHub username: MarcHLev
- Project title: VibeCheck
- Application purpose: Help people who struggle picking what to listen to when they are feeling certain moods, letting them find the perfect fit for whatever vibe they are feeling.

## How to Run the Application

- Requires Python 3.10+ (developed and tested on Python 3.13). No external packages needed — only the standard library (csv, os, datetime).
- Make sure data/recommendations.txt exists in the project folder.
- Open the project in VS Code (or PyCharm).
- Run vibecheck.py — e.g. python vibecheck.py from the terminal, or use the Run button.
- Follow the prompts to enter your mood and energy level.

## Major Features

- Prompts the user for their current mood and energy level, with input validation and reprompting on invalid or empty entries.
- Matches the mood/energy combination against a set of curated music recommendations (genre, vibe description, and three artists).
- Handles mood/energy combinations that don't have a matching recommendation without crashing.
- Logs every completed session (timestamp, mood, energy, genre) to history.csv.
- Lets the user view their past sessions on demand.
- Supports checking multiple moods in one run via a repeat loop.

## Python Concepts Used

- Functions: the program is broken into single-purpose functions — get_mood(), get_energy(), load_recommendations(), get_recommendation(), display_recommendation(), log_session(), and show_history() — tied together by main().
  
- Collections: a nested dictionary structure (data[mood][energy] = {...}) is used to look up recommendations, and lists are used to store artist names and CSV rows.
  
- Conditionals: input validation, checking whether a mood/energy combination exists in the data, and deciding whether to log a session or continue the loop.
  
- Loops: while True loops handle reprompting on invalid input and let the user check multiple moods without restarting the program.
  
- File persistence: recommendations.txt is read once at startup; history.csv is appended to after every session and read back by show_history().
  
- Exception handling: try/except FileNotFoundError guards file reads in load_recommendations() and show_history() so a missing file doesn't crash the program.

## Data Files

- data/recommendations.txt — pipe-delimited text file, one recommendation per line, in the format: mood|energy|genre|vibe|artist1,artist2,artist3. Loaded once at startup into a nested dictionary keyed by mood, then energy.

- history.csv — created automatically the first time a session is logged. Columns: date (timestamp), mood, energy, genre. Grows by one row per completed session.

## Testing Summary

- Valid input: confirmed valid moods and energy levels are accepted immediately at each prompt.

- Invalid input: entering an unrecognized mood or energy level reprints the valid options and reprompts instead of crashing or accepting bad data.

- Empty input: pressing Enter with no input reprompts correctly, since an empty string never matches the valid-options list.

- Whitespace and casing: input like " HAPPY " is correctly normalized to "happy" via .strip().lower().

- Unmatched mood/energy combination: tested a combo not present in recommendations.txt and confirmed display_recommendation() shows a "no recommendation found" message instead of crashing, and that no session gets logged to history.csv for that attempt. This testing also surfaced a UX issue — the program was still asking "View past sessions?" right after telling the user nothing was found, which felt like a non sequitur. Fixed by only offering the history prompt when a recommendation was actually found, alongside the existing log_session() call.

- Missing recommendations file: temporarily renamed data/recommendations.txt and confirmed the program prints "Could not find recommendations file: ..." and continues running gracefully (every lookup returns None) rather than crashing.

- Persistence across restarts: completed a session, closed the program entirely, restarted it, and confirmed history.csv still contained the earlier session alongside new ones — confirming data actually persists between separate runs rather than just within a single session.

## AI Use

Claude was used only during the AI-assisted improvement pass, after the original working version was committed. It reviewed my finished code and suggested five accepted improvements (malformed-line handling, artist whitespace stripping, graceful Ctrl+C exit, and explanatory comments) and one rejected suggestion (empty-file warning). One suggestion (corrupted history row detection) had to be revised after testing showed Claude's original approach didn't actually work.
