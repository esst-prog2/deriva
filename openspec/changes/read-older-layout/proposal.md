# Proposal: read INEC's older dictionary layout

## Why

The cosmetic/real rule agrees with my hand labels on 12 of 22 changes, and every
description change between 2021 and 2025 happens in one step, so any improved rule could
only be measured on the same 22 labels it was tuned on. The 2026-11-07 spike found an
unseen set: between the 2019-12 and 2020-09 persona dictionaries, 25 of 87 shared
variables changed their question text, and only 4 of those are among the 22 labelled
variables. deriva cannot read those files: they use INEC's older layout, so it stops with
"no header row found". To label that pair blind, deriva has to read it.

## What Changes

- The dictionary reader recognises a second layout: a header row with the cells
  `CODIGO DE LA VARIABLE` and `PREGUNTA`, in any columns. The variable name is read from
  the `CODIGO DE LA VARIABLE` column and the description from the `PREGUNTA` column;
  every other column, including `NOMBRE DE LA VARIABLE`, is ignored.
- The 2021+ layout (`Nombre del campo` in the first column) is read exactly as before.
- When neither header is found, the error names both headers it looked for.
- Everything after reading (alignment, the rule, the CSV, the labels template,
  deriva-eval) is unchanged. The cosmetic/real rule is unchanged.

## Not in this change

- Comparing an older-layout round with a 2021+ round. The spike showed the two layouts'
  text fields do not line up (130 of 149 shared variables differ), so such a comparison
  would report layout differences, not instrument changes. deriva does not prevent it;
  the README says not to rely on it.
- The `NOMBRE DE LA VARIABLE` column. It changed for 76 of 87 variables between
  2019-12 and 2020-09, which looks like a systematic relabelling; left for later.
- Any new classification rule.
