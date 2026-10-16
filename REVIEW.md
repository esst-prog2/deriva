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