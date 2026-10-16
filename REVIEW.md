# Code review (Homework 6)

Whole-repository review of deriva, one kind of problem at a time.
Each section lists what I looked for, what I found, and what I did about it.
Each review is its own commit on the `hw6-review` branch.

## 1. Spec drift

**Looked for:** code that does something no spec requirement describes, and spec
requirements that the code does not build or that no test checks.

**Found:**
- "Punctuation" was not defined. The rule uses Unicode punctuation categories, so `%`
  and `/` are dropped while `>=`, `$` and `°` are kept.
- The labels template prints a "descriptions differing" line the spec did not allow.
- Several behaviours existed only in the code: `,` or `;` delimiter in deriva-eval,
  input errors, disagreement order, row order in the changes CSV, the unchanged count,
  and the error for a description without a name.
- Some requirements had no test.

**Did:**
- Did not change the rule, because the 12 of 22 measurement depends on it. Wrote the
  existing behaviour into the specs instead, with new scenarios.
- Added the missing tests with small invented inputs, not the real files.
- No code in `src/` changed. Specs pass `openspec validate --specs --strict`.

**Left open:** accent removal also folds `ñ` to `n`, so `Año` vs `Ano` counts as
cosmetic. In Spanish these are different words, so this could hide a real change.
Logged, not changed yet.

## 2. Names that are not in the spec

**Looked for:** functions, parameters, constants, options and ideas in `src/deriva/`
that the specs and README never describe.

**Found:** no invented feature. Every name maps to something the spec or README
describes. What the spec did not say: errors go to stderr with exit status 1;
"removing accents" is NFKD folding (so `m²` becomes `m2` and `ñ` becomes `n`);
"ignoring case" is casefold; in deriva-eval the first `description_` column is round A;
and a year inside a longer run of digits was taken as the round label.

**Did:**
- Wrote the error format, NFKD folding, casefold and the round order into the specs.
  The rule itself is unchanged.
- Fixed the year pattern so `ronda_120215` is no longer read as 2021, with a test.
- Left as they are, with no spec change: delimiter choice, trimming of `variable` and
  `note`, formula cells, numeric cells, and "label" meaning both a round name and a
  hand verdict. Each is minor and renaming would touch many files for little gain.

**Moved to a later review:** deriva-eval crashes on a labels file saved as Windows-1252
instead of printing an error (review 5, errors).

## 3. Patched where it broke, not where it was wrong

**Looked for:** chains of commits that fix the same area again and again, or special
cases added one by one on top of a wrong assumption. Read the full `git log` of all
branches, not only the code.

**Found:** no chain of fix commits in `src/`; the code changed only twice. The
pattern shows up in the specs and setup instead:
- The cosmetic/real rule assumes Unicode categories match "does not change what the
  variable measures". Each review found another case where they do not (`%`, `m²`,
  `ñ`), and each time the spec got one more scenario describing what Unicode does,
  not a decision about what the rule should do.
- The round label from the file name now has three fallbacks, but the fix sits in the
  right place (the regex is the rule).
- Workarounds for iCloud and hidden `.pth` files were added wherever a symptom showed
  up: shell hook, pytest config, spike script, one-off command.

**Did:**
- Did not change the rule, because the 12 of 22 measurement depends on it. Updated
  the docstrings in `rule.py` so the code states the same rule as the spec.
- Added a comment on `pythonpath` in `pyproject.toml` and a troubleshooting note in the
  README.
- The fix underneath chain 1 is not another special case in `rule.py`. It is the next
  step of the project: try a different rule and measure it once on a held-out set of
  changes I have not looked at.

  ## 4. A copy instead of a change

**Looked for:** modules, functions, constants or blocks in `src/`, `tests/` and
`spike/` that do almost the same job under different names or in different places.

**Found:** 14 copies. The ones that matter are where changing one place could
silently break or skip another:
- The labels-file columns were written in `output.py` and checked separately in
  `evaluate.py`; renaming one column in the writer would break every new template.
- The description of the normalisation rule (`NORMALISED`) lived in `output.py`,
  away from the rule it describes.
- The tests read CSVs in five ways. `test_hand_labels.py` was a third copy of
  `read_labels`, and one test split rows on line breaks, which breaks descriptions
  that contain a newline.

**Did:**
- One definition of the labels-file columns, shared by writer and reader.
- `NORMALISED` moved next to `normalise()` in `rule.py`; the CSV text is unchanged.
- One `read_csv` helper in `conftest.py`; `test_hand_labels.py` now reads the hand
  labels with `read_labels`, the same way deriva-eval does.
- Left as they are: short repeated blocks in the code (error printing, trimming,
  file names), repeated test helpers that read better inline, and `spike/`, which is
  the record of the 2026-10-05 run.

  ## 5. Errors that disappear

**Looked for:** broad `except`, `except: pass`, `return None` after an error, errors
turned into a default, uncaught exceptions that crash with a traceback, and shell
scripts that carry on after a failure.

**Found:** no broad `except` and no swallowed errors. The problem was the reverse:
each command caught only `DerivaError`, so other errors crashed with a traceback,
and some bad input was silently counted:
- A labels file saved as Windows-1252 or UTF-16, an output CSV that cannot be
  written, and a corrupt or chart-only workbook all crashed with a traceback that
  did not name the file.
- A labels row with a missing field or an unclosed quote was read as "not labelled
  yet", and a variable listed twice was counted twice, both with exit status 0.
  The agreement figure could be wrong without any warning.
- One test passed even when the template run failed, because it did not check the
  return code.

**Did:**
- Each of these now gives a `deriva: error:` or `deriva-eval: error:` message
  naming the file, row or variable, with a test for each and the specs updated.
- The test now checks the return code.
- Left as they are: the console-script test skips when `deriva` is not on PATH
  (it runs under `uv run pytest`), and `spike/run_spike.sh`, which is the record of
  the 2026-10-05 run.