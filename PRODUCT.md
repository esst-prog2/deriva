# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Promo page: one static HTML file, `docs/index.html`, inline CSS and at most a little JS, no build step. Published with GitHub Pages from `main` `/docs`. The tool itself is a Python CLI run with uv.

## Users

Researchers and analysts who use ENEMDU (INEC, Ecuador) microdata across several rounds and want to pool rounds or run a trend. They meet the problem when a variable keeps its name (e.g. `p76`) but its question wording changes between rounds, which nothing in the microdata reveals.

## Product Purpose

deriva compares the variable dictionaries of two ENEMDU rounds and reports which questions were added, removed, reworded cosmetically, or really changed, with both wordings side by side so the researcher makes the call. `deriva-history` builds one searchable page with each persona-module question's wording across nine dictionaries (June 2019 to 2025). Success: a researcher knows what changed before pooling rounds.

## Positioning

It reads INEC's dictionaries as published (changing layouts, file names, column counts), treats the 2021 methodological redesign as a break rather than a change, and was tested against human hand labels made blind, not only against itself. It shows what moved; it never decides comparability for the user.

## Capabilities and Constraints

- `deriva A.xlsx B.xlsx`: counts, CSV with one row per change, real first, both descriptions, reason per verdict.
- `deriva-history data/`: one HTML page; red dot = real change, grey ring = cosmetic, ringed mark = hand-labelled; 2021 redesign shown as a break.
- `deriva --labels-template` + `deriva-eval`: blind hand labelling and agreement report.
- Does not cover: response categories/value labels, renamed variables, harmonising/recoding data, vivienda/hogar dictionaries, pre-2021 vs 2021+ direct comparison.
- Terminology: "round", "dictionary", "real change", "cosmetic change", "redesign break".

## Brand Commitments

- Name: deriva (lowercase).
- Voice: plain, first person singular, honest about limits. English only for now.
- Shared mark meaning across surfaces: red dot = real change, grey ring = cosmetic.
- Nothing personal on public pages: no author name, email, photo or local file paths.

## Evidence on Hand

- 2021 vs 2025 persona: 151 vs 139 variables, 12 removed, 22 descriptions changed.
- Default rule vs blind hand labels on those 22: agreed on 12 of 22, hid no real change.
- Second rule on an unseen pair (Sept vs Dec 2020): 40 of 45, hid none of 7 real changes.
- Real example: `p76`, December 2020, "BONO DE DESARROLLO HUMANO" → "BONO o PENSIÓN"; cosmetic misfile `13er` → `13vo`.
- Content source: PROMO.md. Live demo: the generated history page.
- Absent, never invent: users, testimonials, downloads, stars, institutional endorsement.
- Data: public ENEMDU data from INEC (CC-BY); dictionaries ship in the repo.

## Product Principles

- Show both wordings; the researcher decides.
- Err the safe way: a cosmetic edit flagged as real beats a real change hidden.
- Say who decided each mark: hand label or unchecked rule.
- State limits as plainly as capabilities.
