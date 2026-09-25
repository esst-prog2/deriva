# deriva

Compares the variable dictionaries of two survey rounds and reports what changed
in the instrument between them.

## Usage

Requires [uv](https://docs.astral.sh/uv/). From a clone of this repository:

```
uv sync
uv run deriva "data/Diccionario de Datos_persona_anual_2021.xlsx" "data/Diccionario de Datos_persona_anual_2025.xlsx"
```

The earlier round goes first. deriva prints the number of variables in each round and how
many were added, removed, cosmetically changed and really changed, then writes
`deriva_2021_vs_2025.csv` to the current directory (replacing any earlier copy). Each
round is named by the last year in its file name.

The CSV has one row per change, real changes first:

| column | content |
|---|---|
| `variable` | the variable name |
| `change` | `real`, `cosmetic`, `removed` or `added` |
| `description_2021`, `description_2025` | both descriptions in full; empty for the round the variable is missing from |
| `reason` | why the row was classified that way |

A description change is **cosmetic** when the two descriptions become identical after
removing accents, ignoring case, treating punctuation as spaces and collapsing
whitespace, and **real** otherwise. The rule misfiles some cases (`13er` → `13vo` counts
as real), so read both descriptions before trusting a verdict.

Run the tests with `uv run pytest`.

### Checking the rule against hand labels

To measure how often the cosmetic/real rule agrees with a person, label the description
changes of one pair of rounds by hand, **before** seeing the rule's verdicts on that pair:

1. Generate a blind labels template. This prints only the variable counts and how many
   descriptions differ; it runs no classification and writes no changes CSV.

   ```
   uv run deriva --labels-template "data/Diccionario de Datos_persona_anual_2021.xlsx" "data/Diccionario de Datos_persona_anual_2025.xlsx"
   ```

   It writes `labels_2021_vs_2025.csv`: one row per variable whose description differs
   between the rounds, with both descriptions and empty `label` and `note` columns. It
   refuses to overwrite an existing labels file, so entered labels are never lost.

2. Fill in `label` for each row with `cosmetic` or `real` (case does not matter), and use
   `note` for anything worth remembering. Leave a label empty to skip that row for now.
   Do not run plain `deriva` on this pair until you are done, or its verdicts will
   colour your labels. Saving from Excel is fine, including with `;` as the separator.

3. Compare your labels with the rule:

   ```
   uv run deriva-eval labels_2021_vs_2025.csv
   ```

   It prints how many rows are labelled, a 2×2 table of your label against the rule's
   verdict, the agreement, and every disagreement with both descriptions and your note.
   Disagreements where you said `real` and the rule said `cosmetic` come first: those are
   real changes the rule would hide. With no labels filled in yet it reports
   `0 of 22 rows labelled` and `nothing to measure yet`.

Settle the rule before the first measurement. If you then change the rule because of
what the disagreements show, measure it again on a pair of rounds you have not looked
at, not on the same labels.

**A note on 2021.** INEC made methodological changes to ENEMDU between 2020 and May 2021,
so the 2021 annual round straddles the redesign. Differences between 2021 and later rounds
partly reflect that redesign; do not read their number as ordinary year-to-year drift.

## 1. The demo

I open a terminal and run
`deriva "Diccionario de Datos_persona_anual_2021.xlsx" "Diccionario de Datos_persona_anual_2025.xlsx"`.
It prints that the 2021 round has 151 variables and 2025 has 139: 12 variables were removed,
none were added, and 22 descriptions changed — of which 9 are cosmetic (accents,
capitalisation, stray punctuation) and 13 are real. I open the CSV it wrote next to the
files, and the 13 real ones are there with both descriptions side by side, including `rama1`
moving from CIIU4 to CIIU 4.1 and `p54a` losing the words "trabajo secundario". Then I run
it on 2021 against 2022 and it reports the same 12 removals and zero description changes —
the point being that it does not invent differences where the instrument stayed still.

## 2. The shape

```
in           two ENEMDU variable dictionaries (Excel), one per annual round
out          a printed summary by type of change + a CSV, one row per change
in between   find the header row in each sheet and read the variable names and their
             descriptions; line the two rounds up by variable name; for names present in
             both, compare the descriptions and separate cosmetic differences from real
             ones; count and group what is left
```

## 3. The size

The first useful version:

- takes two dictionary files as command-line arguments
- locates the `Nombre del campo` header row, which does not sit at the top of the sheet
- reports variables added and removed between the two rounds
- for variables present in both, classifies the description as unchanged, cosmetically
  changed, or really changed
- prints the counts and writes one CSV with a row per change, both descriptions and the
  reason it was classified that way

Explicitly not this term:

- response categories and value labels; the dictionary does not contain them, and reading
  them would mean parsing the SPSS files instead
- the microdata itself
- matching variables that were renamed; in the rounds I checked, no variable was renamed,
  so this is not worth building until I see a round where it happens
- deciding whether two variables are *comparable for analysis*; the tool shows what moved
  and the researcher decides what that means
- harmonising or recoding the data so rounds can be pooled
- comparing more than two rounds in one run
- the vivienda/hogar dictionaries; persona first
- a graphical interface

## 4. How we would know it works

- Given a sheet with no `Nombre del campo` header row, it exits with an error saying which
  header it looked for and did not find.
- Given two descriptions that differ only by an accent or by capitalisation, it reports them
  as a cosmetic change and not as a changed question.
- Given the same dictionary compared against itself, it reports zero changes of every kind.

## 5. What could stop this

The sheets are not laid out identically across rounds. The 2021 file has two columns and the
2025 file has four, two of them empty; five rows of metadata sit above the real header; and
the files are not even named consistently — `persona` in 2021 and 2025 but `personas` in
2022, `vivienda_hogar` in 2021 but `vivienda` afterwards. The published zip for 2022 is
called `Dicionario de variables.zip`, missing a c. Any reader I write has to survive this,
and each new round can break it again.

The line between a cosmetic and a real change is a judgement, not a fact. `13er sueldo`
becoming `13vo sueldo` means nothing; `CIIU4` becoming `CIIU 4.1` means a lot; `per cápita`
becoming `por cápita` is a typo the publisher introduced. I plan to normalise accents,
case and punctuation and treat what survives as real, but that rule will misfile some cases,
so the CSV always shows both descriptions and lets the reader overrule it.

This ground is not empty. R packages like `retroharmonize` harmonise several waves of a
survey into a comparable dataset, and projects like Harmony match questionnaire items
across instruments semantically. They solve the step after mine: they assume you already
know what differs and want it reconciled. What I want is the step before — a command that
answers "what moved between these two files" without asking me to set up a harmonisation
scheme first, and that reads the dictionaries as INEC actually publishes them. If a first
week with `retroharmonize` shows it already answers that question, I would rather find out
now than in week ten, and I will say so in the repository.

The data is ENEMDU, the Ecuadorian national employment survey. It is public microdata
published by INEC under a CC-BY licence, free to download and free to show in class, so the
dictionary files can live in the repository. ENEMDU is also the honest test case: the rounds
really do differ, so the tool has something to find. The instrument I most want to point it
at afterwards is not public, which is another reason the demo runs on ENEMDU.
