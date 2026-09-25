# Planning log

2026-09-25 — The demo numbers in the README (151/139/12/22/9/13) are unverified (AI-generated) and are not an acceptance target. — decided by: user
2026-09-25 — The classifier is checked by hand-classifying the description changes between two rounds, running the rule, and measuring agreement and disagreements. — decided by: user (following instructor feedback)
2026-09-25 — Hand-label description changes between 2021 and 2025; keep a middle round pair (2023 or 2024) unseen as a second evaluation set. — decided by: user
2026-09-25 — The ENEMDU persona dictionaries go in data/. — decided by: user
2026-09-25 — The MVP is the CLI, the evaluation script and an empty labels CSV template, due 2026-09-26; filling in the labels is later work, outside the MVP. — decided by: user
2026-09-25 — The tool generates the labels template with the variable name and both descriptions filled in, empty label and note columns, and no rule verdict. — decided by: user (on Claude's recommendation)
2026-09-25 — Python, managed with uv (course requirement). — decided by: user
2026-09-25 — Accepted defaults: CSV and labels template in the current directory with fixed names; variable names matched exactly after trimming; whitespace treated as cosmetic; .xls out of scope. — decided by: user (on Claude's recommendation)
2026-09-25 — Reader: find the header by exact match on "Nombre del campo" in column A, not by fixed row. — decided by: user (on Claude's recommendation)
2026-09-25 — Reader: read only columns A (name) and B (description); ignore any others. — decided by: user (on Claude's recommendation)
2026-09-25 — Reader: skip fully empty rows rather than stopping at the first one. — decided by: user (on Claude's recommendation)
2026-09-25 — Reader: stop with an error if a variable name appears twice in one dictionary. — decided by: user (on Claude's recommendation)
2026-09-25 — Reader: use the first sheet; revisit if a round ships several sheets. — decided by: user (on Claude's recommendation)
2026-09-25 — The counts 151/139/12/22 (2021 vars, 2025 vars, removed, differing descriptions) were checked by Claude against the real files in data/ and become an acceptance test for the reader; the 9 cosmetic / 13 real split stays unverified. — decided by: user
2026-09-25 — The MVP proposal lists the later levels (post-MVP work) without writing specs for them. — decided by: user
2026-09-25 — Change name add-deriva-mvp, with three capabilities: dictionary-reader, round-comparison, classifier-evaluation. — decided by: Claude
2026-09-25 — The labels template is written by `deriva --labels-template A B`, which prints no cosmetic/real verdict and writes no changes CSV. — decided by: Claude
2026-09-25 — deriva never overwrites an existing labels file; it exits with an error instead. — decided by: Claude
2026-09-25 — The evaluation script is a separate command, `deriva-eval <labels.csv>`, that reads the descriptions from the labels file itself and needs no dictionaries. — decided by: Claude
2026-09-25 — Round labels come from the last 19xx/20xx year in the file name (fallback: file stem; _a/_b suffix if both are the same); outputs are deriva_<A>_vs_<B>.csv and labels_<A>_vs_<B>.csv. — decided by: Claude
2026-09-25 — The changes CSV lists added, removed, cosmetic and real rows (not unchanged), with columns variable, change, description_<A>, description_<B>, reason. — decided by: Claude
2026-09-25 — Normalisation: strip accents, casefold, punctuation becomes a space, collapse whitespace; symbols such as % and $ are kept. — decided by: Claude
2026-09-25 — Names are matched case-sensitively; names differing only in case count as different variables. — decided by: Claude
2026-09-25 — openpyxl (not pandas) for reading; CSVs written as UTF-8 with BOM; deriva-eval accepts , or ; delimiters. — decided by: Claude
2026-09-25 — Exit codes: 0 when a comparison or evaluation completes (changes found or not), 1 for deriva errors, 2 for usage errors. — decided by: Claude
2026-09-25 — data/ is committed so the tests and demo run from a fresh clone. — decided by: Claude
