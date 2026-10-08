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
2026-09-25 — On this machine deriva's uv virtualenv lives in ~/.venvs/deriva (UV_PROJECT_ENVIRONMENT, set by a ~/.zshrc hook only inside the project folder), because iCloud Drive syncs Documents and breaks .venv. — decided by: user (on Claude's recommendation)
2026-09-25 — pytest puts src/ on the import path itself, so the tests do not depend on the editable install. — decided by: Claude
2026-09-25 — add-deriva-mvp archived; its three specs (dictionary-reader, round-comparison, classifier-evaluation) become the project's main specs. — decided by: user
2026-10-05 — hw4 spike question (branch hw4-spike): does deriva load the 2022, 2023 and 2024 persona dictionaries in data/ without code changes? — decided by: user
2026-10-05 — Spike answer criterion: how many of the 3 load (run against 2021), plus the first error for each that fails; no code changes; full terminal output saved to spike/output.txt. — decided by: user
2026-10-05 — The spike runs deriva in --labels-template mode (same reader path, no cosmetic/real verdicts) with outputs in a temp dir, so the held-out 2023/2024 pair stays unseen. — decided by: Claude
2026-10-05 — Spike answer: 3 of 3 (2022, 2023, 2024) persona dictionaries load without code changes; no errors. 2021 vs 2022: 151/139 vars, 0 added, 12 removed, 0 descriptions differ; 2021 vs 2023: 151/141, 2 added, 12 removed, 0 differ; 2021 vs 2024: 151/139, 0 added, 12 removed, 22 differ. — decided by: user (from Claude's spike run)
2026-10-05 — Spike: 2024 vs 2025 are identical in content (139/139 vars, 0 added, 0 removed, 0 descriptions differ), so all 22 description changes happen between 2023 and 2024. — decided by: user (from Claude's spike run)
2026-10-05 — Held-out plan (2023 or 2024 middle pair) dropped: no pair of the 2021–2025 persona dictionaries gives description changes independent of the 2021 vs 2025 labels set; where the held-out set comes from instead is still open. — decided by: user
2026-10-05 — Download links for the 2022–2024 dictionaries are kept in spike/sources.md. — decided by: user
2026-10-05 — Definition of a real change for the hand labels: a researcher comparing the two rounds would need to check whether the variable still measures the same thing. — decided by: user
2026-10-05 — Labelling process: the user hand-labelled all 22 differing 2021 vs 2025 pairs in the blind template; Claude pointed out the differences between descriptions but gave no verdicts; the rule was not changed before measuring. — decided by: user
2026-10-05 — Hand labels and deriva-eval output are committed as eval/labels_2021_vs_2025.csv and eval/result.txt. — decided by: user
2026-10-05 — Result: by hand 19 cosmetic and 3 real (p54a, p77, rama1); agreement with the rule 12 of 22; 0 cases hand-real / rule-cosmetic; 10 cases hand-cosmetic / rule-real. The rule's own split is 9 cosmetic / 13 real, the same as the unverified README figure. — decided by: user (numbers re-checked by Claude with deriva-eval)
2026-10-05 — A second coder (Claude) agreed with the hand labels on 21 of 22 pairs, differing only on p78. — decided by: user
2026-10-05 — README demo: the unverified 9 cosmetic / 13 real replaced with the hand-label result and the agreement figures. — decided by: user
2026-10-05 — The rule is not changed after this measurement. — decided by: user
2026-10-05 — Correction to the second-coder entry above: Claude's labels were not independent, because Claude had seen the user's labels before giving its own, so the 21 of 22 must not be read as inter-rater agreement. — decided by: user
2026-10-08 — hw5 (branch hw5-usable) test sentence: "A test would go red if the rule labelled any of the 3 changes I judged real by hand (p54a, p77, rama1) as cosmetic." — decided by: user
2026-10-08 — Expected value for that test: p54a, p77 and rama1 are real; it comes from the user's blind hand labels in eval/labels_2021_vs_2025.csv, made before seeing the rule's verdicts, not from running the code. The test is not written yet. — decided by: user
2026-10-08 — The hw5 test is tests/test_hand_labels.py: it reads the hand labels from eval/labels_2021_vs_2025.csv, checks that the rows labelled real are exactly p54a, p77 and rama1, and checks that the rule gives each of them its hand label. — decided by: Claude
2026-10-08 — Breaking change used to show the test going red: src/deriva/rule.py line 24, `chars.append(" " if category.startswith("P") else ch)` changed to `chars.append(" " if category.startswith("P") or category == "Nd" else ch)`, so digits are dropped like punctuation and rama1 (CIIU4 vs CIIU 4.1) becomes cosmetic. — decided by: user (asked for rama1 to become cosmetic); exact line chosen by Claude
2026-10-08 — Red run (uv run pytest with that line changed): 6 failed, 51 passed; test_rule_agrees_with_hand_label[rama1] fails with 'cosmetic' == 'real', while p54a and p77 still pass; the other 5 failures are existing tests that also use CIIU4 vs CIIU 4.1. Output saved to eval/hw5_red.txt. — decided by: user (from Claude's run)
2026-10-08 — Green run (line 24 put back): 57 passed. Output saved to eval/hw5_green.txt. — decided by: user (from Claude's run)
2026-10-08 — Step 6 (real use) expectation, logged before running: plain deriva on 2023 vs 2024 should report 141 variables in 2023, 139 in 2024, 0 added, 2 removed, 22 descriptions differing, with the rule calling 9 cosmetic and 13 real. Source: the spike (2021 vs 2023 had 2 added, 2021 vs 2024 had 0 added, 2022 and 2023 match 2021, 2024 matches 2025) and the rule's split in eval/result.txt, not a run of deriva on this pair. — decided by: user
