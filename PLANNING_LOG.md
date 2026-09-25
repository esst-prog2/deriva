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
