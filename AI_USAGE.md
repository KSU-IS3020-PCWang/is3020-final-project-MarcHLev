# AI Improvement Record

## Original Development

I wrote all seven core functions myself — get_mood(), get_energy(), load_recommendations(), get_recommendation(), display_recommendation(), log_session(), show_history(), and main() — before the first required commit ("Original working version before AI improvement").

AI use during this stage was limited to conceptual guidance, not code: I asked Claude to explain the logic I should implement for each function (e.g. "loop until valid input, strip and lowercase, check membership, reprompt if invalid" for get_mood()/get_energy(), or "check if mood in data first, then if energy in data[mood]" for get_recommendation()). Claude did not write any function bodies — I wrote every line of code myself and pasted it back for review after each one. Claude's role at this stage was to review my finished functions for correctness (e.g. confirming get_recommendation()'s guard clause and return contract were right) and to help debug a couple of environment issues (unsaved file changes not showing in Git, a path issue when running the script).

## AI Tools Used

Claude (Anthropic), used through the chat interface only — no autocomplete or inline code generation.

## Improvements Requested

After the original working version was committed, I asked Claude to review the whole file for input validation gaps, try/except coverage, docstring/comment quality, and edge cases.

## Changes Accepted

Malformed line handling in load_recommendations(): wrapped the line.split("|") unpack in try/except ValueError so a line with the wrong number of fields is skipped with a message instead of crashing the whole program. Accepted because a hand-edited data file is a realistic failure case my original version didn't handle. Verified by adding a broken line to recommendations.txt, confirming the program printed a skip message and the rest of the file still loaded correctly.

Artist whitespace stripping: changed artists_string.split(",") to a list comprehension with .strip() on each piece, since splitting alone left a leading space on artists after the first. Accepted because it directly fixed a real display bug I could see in my own output. Verified by running a session and visually confirming no stray spaces in the printed artist list.

Graceful Ctrl+C handling in main(): wrapped the loop body in try/except KeyboardInterrupt, printing "Goodbye!" and breaking instead of letting Python print a raw traceback. Accepted because it's a small, low-risk usability improvement. Verified by pressing Ctrl+C mid-prompt and confirming the clean exit.

Inline comments on non-obvious logic: added short comments explaining why the nested-dict initialization check exists in load_recommendations(), and why the file_exists check in log_session() has to happen before opening the file. Accepted because both spots involve reasoning that isn't obvious just from reading the code, and my rubric specifically asks for comments on non-obvious logic.

## Changes Rejected or Revised

Rejected
Empty-file warning: Claude suggested printing a warning if recommendations.txt loads but has zero valid lines. I rejected this because an empty data file already results in every lookup returning None, which my program already handles gracefully via display_recommendation()'s "no recommendation found" message — the extra warning didn't add enough value for the added code.

Revised
Corrupted history row guard: Claude's original suggestion for show_history() was to wrap the row-printing logic in try/except KeyError, on the assumption that a corrupted/short row in history.csv would raise a KeyError. When I tested this, it silently failed — the program printed energy Pop → None instead of skipping the row. I investigated and found that csv.DictReader fills missing trailing fields with None (its restval default) rather than omitting the key, so row['genre'] never actually raises KeyError — it just sometimes holds None. I rewrote the guard as an explicit check, if None in (row['date'], row['mood'], row['energy'], row['genre']), which tests for the real failure mode. Re-tested with the same corrupted row and confirmed the correct skip message now prints.

## What I Learned

Going in, I honestly expected to just rubber-stamp whatever Claude suggested — the code looked reasonable, it used a pattern I already recognized (try/except around a dict access), and I didn't think there was much to question. The KeyError guard for #4 is what changed that. It read like it should obviously work, and then when I actually broke a row on purpose and ran it, it just... didn't. No crash, no skip message, just a quiet None sitting where the genre should've been, like nothing had gone wrong at all.

That was the surprising part — I assumed a missing field in a CSV row would blow up when you tried to access it by key, the same way a missing dictionary key normally would. Turns out csv.DictReader is more forgiving than that: it pads short rows with None instead of just leaving the key out, which means the exact failure mode I was trying to catch never actually raises an exception at all. It's a small, specific detail, but it completely changes what kind of check will actually catch the problem — you can't guard against an exception that's never thrown.

The bigger lesson is less about csv specifically and more about how I should treat AI-suggested code going forward: it has to earn its place by actually surviving a test, not just by looking plausible or matching a pattern I recognize. If I'd accepted the KeyError version as-is, I would've shipped a "guard" that did absolutely nothing — the code would've looked defensive without being defensive at all. Rerunning the same test after every change, especially the ones I already feel confident about, is apparently just the actual cost of trusting anything, AI-written or not.Explain what you learned by reviewing and applying the AI-assisted improvements.
