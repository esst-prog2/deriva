# deriva — promo page content (draft)

Audience: researchers and analysts who use ENEMDU across several rounds.

---

## Headline

**Know what changed in the questionnaire before you pool the rounds.**

## Subheadline

deriva compares the variable dictionaries of two ENEMDU rounds and tells you which
questions were added, removed, reworded cosmetically, or really changed — with both
wordings side by side, so you make the call.

## The problem

You want to run a trend from 2019 to 2025. The variable is called `p76` in every round,
so it must be the same question. It isn't: in December 2020 "BONO DE DESARROLLO HUMANO"
became "BONO o PENSIÓN". Nothing in the microdata tells you that. The only way to find out
is to open each round's dictionary and read the questions one by one.

INEC doesn't make that easy. The dictionaries change layout, file names and column counts
from round to round, and the 2021 methodological redesign breaks the series in the middle.

## What deriva does

- **Compare two rounds.** `deriva 2021.xlsx 2025.xlsx` reads both dictionaries as INEC
  publishes them and reports 151 vs 139 variables, 12 removed, 22 descriptions changed. It
  writes a CSV with one row per change, real changes first, both descriptions, and the
  reason for each verdict.
- **See every question's history.** `deriva-history data/` turns nine persona dictionaries
  (June 2019 to 2025) into one searchable page. Search a variable and you see its wording in
  every round, each change marked, and the 2021 redesign shown as a break rather than as a
  change.
- **Check the rule yourself.** `deriva --labels-template` gives you a blank sheet to label
  the changes by hand, without seeing the tool's verdicts first. `deriva-eval` then shows
  where you and the rule agree, and lists every disagreement.

## Why you can trust it (and where you shouldn't)

"Cosmetic" or "real" is a judgement call, so deriva was tested against human judgement,
not just against itself:

- On 2021 vs 2025 I labelled all 22 changes by hand before running the rule. The default
  rule agreed on 12 of 22 and **never hid a real change**. Its mistakes go the safe way: it
  flags cosmetic edits like `13er` → `13vo` as real.
- A second rule, tested on a pair of rounds it had never seen (Sept vs Dec 2020), agreed on
  40 of 45, again hiding none of the 7 real changes.
- On the history page, every mark says who decided it: my hand label where I made one, the
  rule (unchecked) everywhere else.

deriva shows you what moved. Whether two rounds are still comparable for your analysis is
your decision.

## What it doesn't do (yet)

- Response categories and value labels (they aren't in the dictionaries)
- Renamed variables
- Harmonising or recoding the data so the rounds can be pooled. That's the next step, and
  tools like `retroharmonize` already do it
- The vivienda/hogar dictionaries. It covers the persona module for now
- Comparing a pre-2021 round with a 2021+ round directly (the layouts don't line up)

## Get started

1. Install [uv](https://docs.astral.sh/uv/).
2. Clone the repository:

   ```
   git clone https://github.com/esst-prog2/deriva
   cd deriva
   ```

3. Install and run:

```
uv sync
uv run deriva "data/Diccionario de Datos_persona_anual_2021.xlsx" "data/Diccionario de Datos_persona_anual_2025.xlsx"
uv run deriva-history data/
```

Built on public ENEMDU data from INEC (CC-BY). The dictionaries are in the repository, so
the demo runs from a fresh clone.
