# deriva — promo page content

Audience, two readers:

1. Analysts and evaluators who build indicators and reports across ENEMDU rounds and can
   run deriva (questions 4 and 5).
2. People who compare results and only need to look up whether a question changed before
   using it. For them the history page is the product, with no install (question 3).

---

## 1 · Headline

**Is it still the same question? Find out without going back and forth between codebooks.**

## Subheadline

deriva reads the variable dictionaries (codebooks) of ENEMDU rounds and tells you which
questions were added, removed, reworded cosmetically or really changed, with both wordings
side by side, so you decide whether the rounds still compare. It covers the persona module,
from June 2019 to 2025.

Main button: Open the history of `p76`. Under it: "If you would rather run it yourself, go
to question 4." Then the 30-second video.

Skip: If you already know the problem, go to question 3 to look a question up, or question 4
to run deriva.

## 2 · Is `p76` the same question in every round?

You want to run a trend from 2019 to 2025. The variable is called `p76` in every round,
so it must be the same question. It isn't: in December 2020 "BONO DE DESARROLLO HUMANO"
became "BONO o PENSIÓN". Nothing in the microdata tells you that, and a check that matches
variable names won't either, because the name never changed. The only way to find out is to
open each round's dictionary and read the questions one by one.

(The wording of `p76` in nine dictionaries, as deriva-history shows it.)

INEC doesn't make that easy. The dictionaries change layout, file names and column counts
from round to round, and the 2021 methodological redesign breaks the series in the middle.
Each dictionary gives you one round's wording; it doesn't say what changed since the round
before.

Skip: Only need to check a question before you use it? Go to question 3. Comparing
dictionaries for your own indicators? Go to question 4.

## 3 · Need to check one question before you use it?

Open the history page and type a variable name, such as `p76`. You see its wording in every
round it appears in, from June 2019 to 2025, with each change marked: a red dot for a real
change, a grey ring for a cosmetic one, a double ring where I checked it by hand, and a dash
where the variable was added or removed. The 2021 redesign is shown as a break, not
compared. Click a row to read every version in full.

Don't know the variable name? Choose "All variables" and scroll: each row shows the name
next to a short form of the question.

There is nothing to install. It runs in your browser.

Button: Open the history page.

Skip: If you want to know how far to trust the marks, go to question 5.

## 4 · Building indicators across rounds?

Run deriva on two dictionaries and you get the whole list, not one question at a time.

- **a · Compare two rounds.** `deriva 2021.xlsx 2025.xlsx` reads both dictionaries as INEC
  publishes them and reports 151 vs 139 variables, 12 removed, none added, 22 descriptions
  changed. It writes a CSV with one row per change, real changes first, both descriptions,
  and the reason for each verdict.
- **b · Build the history page yourself.** `deriva-history data/` turns every persona
  dictionary in a folder into one searchable page, like the one in question 3.
- **c · Check the rule yourself.** `deriva --labels-template 2021.xlsx 2025.xlsx` gives you
  a blank sheet to label the changes by hand, without seeing the tool's verdicts first.
  `deriva-eval labels_2021_vs_2025.csv` then shows where you and the rule agree, and lists
  every disagreement.

### Run it on your machine

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

The dictionaries are in the repository, so this runs from a fresh clone.

Skip: If you want proof before running it on your own rounds, go to question 5.

## 5 · Can you trust its verdicts?

"Cosmetic" or "real" is a judgement call, so deriva was tested against human judgement,
not just against itself:

- On 2021 vs 2025 I labelled all 22 changes by hand before running the rule. The default
  rule agreed on 12 of 22 and **never hid a real change**. Its mistakes go the safe way: it
  flags cosmetic edits like `13er` → `13vo` as real.
- A second rule, tested on a pair of rounds it had never seen (Sept vs Dec 2020), agreed on
  40 of 45, again hiding none of the 7 real changes.
- On the history page, every red dot and grey ring says who decided it: my hand label where I
  made one, the second rule (unchecked) everywhere else. Added, removed and same marks come
  straight from the dictionaries.

deriva shows you what moved. Whether two rounds are still comparable for your analysis is
your decision.

Skip: To see what it doesn't cover, go to question 6.

## 6 · What doesn't it do (yet)?

- Other surveys, and ENEMDU's vivienda/hogar dictionaries. It reads the persona
  dictionaries only, for now
- Response categories and value labels (they aren't in the dictionaries)
- Renamed variables
- Comparing a pre-2021 round with a 2021+ round directly (the layouts don't line up)
- Harmonising or recoding the data so the rounds can be pooled. That's the next step, and
  tools like `retroharmonize` already do it

## Footer

Built on public ENEMDU data from INEC (CC-BY). Code on GitHub.
