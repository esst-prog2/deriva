# deriva

Compares the variable dictionaries of two survey rounds and reports what changed
in the instrument between them.

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
