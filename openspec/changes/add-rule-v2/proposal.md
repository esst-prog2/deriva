# Proposal: an optional second cosmetic/real rule

## Why

On both labelled pairs the first rule never hides a real change but over-flags:
12 of 22 agree on 2021 vs 2025, 2 of 24 on 2019-12 vs 2020-09. Most misses fall into a
few patterns I labelled cosmetic: a different reference month (21 of the 22 misses on
2019 vs 2020), the variable's own code repeated at the start of the text, and
abbreviated ordinals (13er / 13vo).

## What Changes

- New module `deriva.rule_v2` with `classify_v2(a, b, variable)`: the first rule's
  normalisation, plus those three patterns treated as cosmetic.
- `deriva-eval --rule v2` measures it against a labels file; the report starts with
  `rule: v2`. Without `--rule`, or with `--rule v1`, everything is as before.
- The first rule, the `deriva` command, its CSV and the demo's 12 of 22 are unchanged.

## How it will be judged

v2 was built after seeing both labelled pairs, so its numbers there only show the fit:
14 of 22 on 2021 vs 2025 and 24 of 24 on 2019 vs 2020, still with 0 real changes
called cosmetic. It is measured once, on a third pair labelled blind before v2 is run
on it. If it hides a real change there, it is not adopted.
