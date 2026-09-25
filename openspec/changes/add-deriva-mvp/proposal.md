# Proposal

## Why

Researchers comparing two ENEMDU rounds have no quick way to see what moved in the
instrument: they diff the INEC variable dictionaries by eye, and the dictionaries are
laid out inconsistently. deriva answers "what moved between these two files" from the
dictionaries as INEC publishes them (README sections 1–3). Its cosmetic-vs-real rule is
a judgement, so the MVP also ships a way to measure that rule against hand labels
(following instructor feedback) instead of trusting it. Due 2026-09-26.

## What Changes

- New `deriva` command-line tool, run as `deriva <dict_A.xlsx> <dict_B.xlsx>`:
  - reads each ENEMDU persona dictionary, locating the `Nombre del campo` header row
    wherever it sits
  - lines the two rounds up by variable name and reports variables added and removed
  - for variables in both rounds, classifies the description as unchanged, cosmetically
    changed (differs only in accents, case, punctuation or whitespace) or really changed
  - prints counts by type of change and writes one CSV with a row per change, both
    descriptions and the reason for the classification
- A labels-template mode of the same command that writes a CSV of every variable whose
  description differs (name + both descriptions, empty `label` and `note` columns) and
  shows **no** rule verdict, so labelling stays blind.
- New `deriva-eval` evaluation script: reads a labels CSV, runs the rule on each labelled
  pair and reports the agreement table and every disagreement. With no labels filled in
  it reports that there is nothing to measure yet.
- A Python project managed with uv, with tests, including an acceptance test on the real
  2021 and 2025 dictionaries in `data/`: 151 and 139 variables, 12 removed, 0 added,
  22 descriptions differing. The 9 cosmetic / 13 real split in the README is unverified
  and is **not** a test target.

Out of scope for this change (unchanged from README section 3): response categories,
microdata, renamed variables, comparability judgements, harmonisation, more than two
rounds per run, vivienda/hogar dictionaries, a GUI, `.xls` input.

## Later levels

Listed for direction only; none of these get specs in this change.

1. **Label 2021 vs 2025** — the user hand-labels the generated template blind, runs
   `deriva-eval`, and writes up each disagreement. The rule is frozen before this first
   measurement.
2. **Held-out measurement** — pick the unseen middle pair (2023 or 2024). First count its
   differing descriptions without looking at verdicts; both rounds post-date the
   May 2021 methodological change, so it may have too few differences to be useful.
   Measure the frozen rule on it.
3. **Rule revisions** — adjust the normaliser where disagreements show a pattern (e.g.
   ordinal suffixes `13er`/`13vo`), then re-measure on the held-out pair only.
4. **retroharmonize check** — the README's go/no-go: does `retroharmonize` already answer
   "what moved"? Record the answer in the repository.
5. **More rounds** — run all consecutive annual pairs; verify the claim that 2021 vs 2022
   has zero description changes.
6. **vivienda/hogar dictionaries** — extend the reader to the other dictionary files.
7. **Deferred until evidence appears** — renamed-variable matching, multi-sheet
   workbooks, `.xls` input, more than two rounds per run.

## Capabilities

### New Capabilities

- `dictionary-reader`: reading one ENEMDU variable dictionary workbook into a set of
  variable names and descriptions, with clear errors for unreadable layouts.
- `round-comparison`: the `deriva` command — aligning two rounds, classifying description
  changes, the printed summary and the changes CSV.
- `classifier-evaluation`: the blind labels template and the `deriva-eval` agreement
  report.

### Modified Capabilities

None; the project has no specs yet.

## Impact

- New Python package and `pyproject.toml` (uv), with `openpyxl` as the only runtime
  dependency and `pytest` for development.
- Two console commands: `deriva` and `deriva-eval`.
- `data/` holds the 2021 and 2025 persona dictionaries (CC-BY, INEC) and is committed so
  the acceptance test and the demo run from a fresh clone.
- README gains usage for both commands and a note that the 2021 round straddles the
  May 2021 ENEMDU methodological change.
