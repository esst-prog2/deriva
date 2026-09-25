# Design

## Context

Greenfield: the repository holds only the README brief, `PLANNING_LOG.md` and the two
real dictionaries in `data/`. Both are single-sheet `.xlsx` files (`Hoja1`) with five
metadata rows, the header in row 6 column A, clean string cells and no duplicate names;
2025 adds two empty columns and eleven trailing empty rows. Python via uv is a course
requirement. One day of build time, so the design favours the fewest moving parts.
Motivation: see proposal.md. Behaviour: see the three specs.

## Goals / Non-Goals

**Goals:**
- One rule implementation shared by `deriva` and `deriva-eval`, so the evaluation
  measures exactly what the tool does.
- Each stage (read, align, classify, write) testable on its own without Excel files,
  plus end-to-end tests on the real files.

**Non-Goals:**
- Configurable normalisation, output directories or column mappings.
- Packaging for PyPI; the tool runs from a clone with `uv run`.

## Decisions

**Layout.** `src/deriva/` package with modules:

```
reader.py     path -> Dictionary(label, variables: dict[name, description])
compare.py    two Dictionaries -> Comparison (added, removed, per-variable verdicts)
rule.py       normalise(text) and classify(desc_a, desc_b) -> unchanged|cosmetic|real
output.py     changes CSV, labels template CSV, printed summary
cli.py        argparse entry point for `deriva`
evaluate.py   entry point for `deriva-eval`
```

Pipeline: `cli -> reader (x2) -> compare -> rule -> output`; `evaluate -> rule`.
Both console scripts are declared in `pyproject.toml` `[project.scripts]`. Alternative
considered: one command with subcommands (`deriva compare`, `deriva eval`); rejected
because the README demo fixes `deriva A B` as the interface.

**Excel library: openpyxl, not pandas.** The reader walks cells to find a label, which is
a row loop, not a dataframe operation; openpyxl is one small dependency. Workbooks are
opened with `read_only=True, data_only=True` so formulas yield their values.

**Normalisation** (`rule.normalise`): Unicode NFKD, drop combining marks, `casefold()`,
replace every Unicode punctuation character (category `P*`) with a space, collapse
whitespace runs to one space, strip. Punctuation becomes a space rather than being
deleted so that `CIIU 4.1` normalises to `ciiu 4 1` and stays distinct from `CIIU4`
(`ciiu4`); deleting it would give `ciiu 41`, which is equally distinct but hides why.
Known cost: `4.1` vs `4,1` counts as cosmetic, accepted. Symbols such as `%` or `$`
(category `S*`) are kept, since they can carry meaning.

**Classify only after an exact-string check.** `unchanged` means byte-identical after
reading, so the labels template (which lists every non-identical pair) and the
`unchanged` class are defined by the same test and cannot drift apart.

**Round labels** come from the last `(19|20)\d\d` match in the file stem; fall back to
the stem; add `_a`/`_b` on a collision. Keeps output names short (`deriva_2021_vs_2025.csv`)
without a `--label` option.

**CSV encoding: `utf-8-sig`.** Excel on macOS and Windows misreads accents in UTF-8
without a byte-order mark; Python's `csv` module reads `utf-8-sig` transparently, so
`deriva-eval` accepts files saved back from Excel. Written with `csv.writer`
(minimal quoting) so descriptions with commas survive.

**Labels template is a flag on `deriva`, not a separate command.** It needs the same
reading and alignment; the flag only switches the output stage and suppresses the
classifier. The labels file is opened with mode `"x"` so an existing file is never
truncated.

**deriva-eval reads descriptions from the labels file** rather than re-reading the
dictionaries. The labelled file is then a self-contained record of what was judged, and
evaluation needs no path bookkeeping. Description columns are found by the `description_`
prefix (exactly two expected), so any round labels work.

**Errors.** A small `DerivaError` exception carries the user-facing message; `cli.main`
and `evaluate.main` catch it, print `deriva: error: <message>` to stderr and exit 1.
argparse usage errors exit 2. Nothing else is caught, so bugs keep their traceback.

**Tests** (pytest): unit tests build small workbooks in `tmp_path` with openpyxl to cover
each reader scenario; the rule is tested on string pairs; end-to-end tests run the CLI
on `data/` for the 151/139/12/0/22 counts, the self-comparison zeros and the 22-row
template, and assert no verdict words in template-mode output.

## Risks / Trade-offs

- [Seeing verdicts before labelling biases the labels] → template mode prints no
  verdicts; the README tells the labeller to generate the template before running plain
  `deriva` on that pair. The tests themselves assert only the 22 total, not the split.
- [Future rounds change layout (header text, sheet order)] → errors name the file and
  what was expected, so a break is visible, not silent; fix when seen (later levels).
- [Excel re-saves the labels file with a different delimiter (e.g. `;` in
  Spanish-locale Excel)] → `deriva-eval` sniffs the delimiter with `csv.Sniffer` over
  `,` and `;`; if the expected columns are still not found it errors naming them.
- [The rule misfiles cases like `13er` → `13vo` or `per` → `por`] → accepted by design;
  measured by `deriva-eval`, revised only in later levels on the held-out pair.
- [2021 straddles the May 2021 ENEMDU methodological change] → documented in the README
  so the 2021 vs 2025 difference count is not read as ordinary year-to-year drift.
