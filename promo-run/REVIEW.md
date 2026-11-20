# Review: "One run, start to finish" (30 s, silent)

## Creative calls
- Storyline B of three (A: a trend chart with a jump, which would have needed an illustrative
  chart; C: today plus a labelled "not built yet" future). B is the only one made entirely of
  real screens.
- Captions carry everything; no audio at all (the page plays the video muted).
- Real changes shown in the table: `rama1` (CIIU4 → CIIU 4.1, hand-labelled real) and
  `p44j` (13er → 13vo, flagged real by the rule, hand-labelled cosmetic) to show the rule errs safe.

## What is real and what was changed
- Terminal text is the exact stdout of `deriva` and `deriva-history` on 2026-11-20, drawn as
  text in a terminal window, not a screen recording. The one substitution: absolute paths
  are shown as `~/deriva/…` (no user name or local folder on a public page).
- The table is the real first 13 rows of `deriva_2021_vs_2025.csv`, cells cut at column edges.
- The browser frame shows a Chrome screenshot of the generated `deriva_history.html?q=p76`.
- Added text: captions and the two "IN ENGLISH" glosses.

## Measured vs looked at
- `hyperframes check`: passes. Frames looked at: 0, 2.5, 5, 8, 11, 14, 18, 21.5, 23, 25,
  28.5, 29.75 s, the review beat sheet, the phone sheet, and four frames pulled from the MP4.
- No sound to check.

## Warnings kept on purpose
- `film_silent`: asked for a video that works without sound; the page autoplays nothing and starts muted.
- `text_below_floor`: the CSV cells (25-26 px) are screen texture; the glosses (30 px) carry the read.
- `line_unread` on the `deriva-history` output (0.9 s): the caption says what it did.
- `content_overlap` at 22.1 s: the browser crossfades over the terminal.

## Weakest shot and what I'd change with more time
- 20-22 s, the second terminal: short and a little empty. A real screen recording of typing
  `p76` into the search box would be stronger than the cut to an already-searched page.

## Revision 2 (2026-11-20)
- New 4.5 s opening: "Comparing a survey across years?" and the user's line under it, over real
  excerpts (rows p74b-p77) of four persona dictionaries (2019-06, 2020-12, 2021, 2025) in their own
  layouts, brought to the front in turn with the p76 row lit each time.
- "151 questions" → "151 variables".
- deriva-history's "11 real changes" and the page's "10 questions changed" are both marked, under
  the caption "All rounds, 2019 to 2025: 11 real changes in 10 questions." (estrato changed twice,
  Sept 2020 and Dec 2020; the CLI counts changes, the page counts variables with one).
- Time made up by cutting the p44j example from the table (rama1 kept), tightening the run
  (8.6 s) and the end card (2.2 s). Total still 30.0 s.
- Kept warnings: the opening's second line (16 words in about 4 s) is under the reading floor
  of 5.3 s; the closing URL is on screen 1.96 s against a 2.0 s floor.
