# Tasks

## 1. Project setup

- [ ] 1.1 Initialise the uv project with a `src/deriva/` package, `openpyxl` as dependency, `pytest` as dev dependency, and `deriva` / `deriva-eval` console scripts; verify `uv sync` succeeds and `uv run pytest` runs (zero tests collected is fine)
- [ ] 1.2 Add a `.gitignore` for `.venv/`, caches and generated `deriva_*.csv` / `labels_*.csv` in the repo root, and commit `data/` with the two dictionaries; verify `git status` shows `data/` tracked and no generated files

## 2. Rule

- [ ] 2.1 Implement `rule.normalise` and `rule.classify` (unchanged / cosmetic / real) as in design.md; verify with pytest cases for every classification scenario in the round-comparison spec (accent, case, punctuation and spacing, `CIIU4` vs `CIIU 4.1`, removed words, identical strings)

## 3. Reader

- [ ] 3.1 Implement `reader.read_dictionary(path)` returning the round label and name→description mapping, with `DerivaError` for missing header, duplicate name and missing/unreadable file; verify with pytest workbooks built in `tmp_path` covering every dictionary-reader scenario (header at row 6 and row 2, extra empty columns, trailing and interleaved empty rows, verbatim descriptions, missing header message naming file and `Nombre del campo`, duplicate `p54a`, missing path)
- [ ] 3.2 Implement round labelling (last 19xx/20xx year in the stem, stem fallback, `_a`/`_b` on collision); verify with pytest on the real file names, a name without a year and a same-file pair
- [ ] 3.3 Add the acceptance test on `data/`: verify 151 variables for 2021 and 139 for 2025

## 4. Comparison and deriva command

- [ ] 4.1 Implement `compare` (added, removed, per-variable verdict for shared names, exact case-sensitive matching); verify with pytest on in-memory dictionaries for added, removed and case-differing names
- [ ] 4.2 Implement the changes CSV writer (`deriva_<A>_vs_<B>.csv`, columns and reasons per spec, `utf-8-sig`, unchanged rows omitted) and the printed summary; verify with pytest reading the CSV back, including a header-only file for a self-comparison
- [ ] 4.3 Wire `cli.main` for `deriva A B` with argparse, `DerivaError` → stderr + exit 1; verify end-to-end with pytest (subprocess or `main([...])` in `tmp_path` as cwd): real files give 151 / 139 / 12 removed / 0 added / cosmetic+real = 22 and exit 0; same file twice gives all zeros; one argument exits non-zero with usage; a sheet without the header exits non-zero naming the header
- [ ] 4.4 Document `deriva A B` usage and output in the README, plus the note that the 2021 round straddles the May 2021 ENEMDU methodological change; verify the documented command runs as written from a fresh `uv sync`

## 5. Labels template

- [ ] 5.1 Add `--labels-template` to `deriva`: write `labels_<A>_vs_<B>.csv` (variable, both descriptions, empty label and note) with exclusive-create, skip the classifier and the changes CSV, print only counts and the path; verify end-to-end on the real files that the template has 22 rows with empty label/note, that no changes CSV is written, that stdout and the file contain no `cosmetic`/`real` verdicts, and that a second run exits non-zero leaving the existing file byte-identical
- [ ] 5.2 Document the labelling workflow in the README (generate the template first, label blind before running plain `deriva` on that pair, allowed labels); verify the documented command runs as written

## 6. Evaluation script

- [ ] 6.1 Implement `deriva-eval <labels.csv>`: read the template format (`utf-8-sig`, `,` or `;` delimiter, description columns by `description_` prefix), validate labels case-insensitively, classify each row with `rule.classify`; verify with pytest that an invalid label `maybe` exits non-zero naming the variable, and that a `;`-delimited file is read
- [ ] 6.2 Implement the report: labelled count out of total, 2×2 table, agreement count and share, and every disagreement with both labels, both descriptions and the note; "nothing to measure yet" with exit 0 when no row is labelled; verify with pytest on a synthetic 22-row file with 10 labelled (8 agree, 2 disagree, including a hand-`real` / rule-`cosmetic` row) and on an empty template
- [ ] 6.3 Document `deriva-eval` usage in the README; verify the documented command runs on a freshly generated template and prints "0 of 22"

## 7. Integration check

- [ ] 7.1 From a fresh clone: `uv sync`, `uv run pytest` all green, then run the README demo (`deriva` on 2021 vs 2025, `deriva --labels-template`, `deriva-eval` on the template) in a scratch directory; verify outputs match the documented counts and generated files land in the current directory
