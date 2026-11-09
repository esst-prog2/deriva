# Proposal: update the December demo

## Why

The demo written in week 1 shows one comparison (2021 vs 2025) and the first rule's
12 of 22. Since then deriva reads INEC's pre-2021 layout, there are three labelled pairs,
and a second rule measured on a pair it never saw agrees with my labels on 40 of 45
changes (the first rule: 20 of 45), hiding none of the 7 real ones. That is the
strongest evidence the project has, and the demo did not show it. I also want the
audience to see the instrument's history, not only one pair: the presentation is
screenshots, and the audience scores the program, so the demo should end on a screen
that shows what the tool is for.

## What Changes

- README section 1 is rewritten (5 sentences): the 2021 vs 2025 run and the 12 of 22
  stay; the second rule's 40 of 45 on September vs December 2020 is added; and a new
  command, `deriva-history data/`, writes `deriva_history.html`, a page with each
  variable's description in every persona dictionary from June 2019 to 2025.
- The 2021 vs 2022 run is dropped from the demo to stay within six sentences.
- New capability `round-history` (spec below), to be built before 1 December.

## Risks

- `deriva-history` does not exist yet; it has about three weeks. If it is not ready,
  the demo falls back to the first three sentences, which already work.
- The older layout and the 2021+ layout cannot be lined up field by field (spike,
  2026-11-07), so the page shows the 2021 redesign as a break, never as a change.
- 40 of 45 rests on one pair; the demo says which pair.
