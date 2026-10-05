# Spec Delta

## Purpose

Measures how often deriva's cosmetic-vs-real rule agrees with a person's hand labels,
using a blind labelling template and an agreement report that lists every disagreement.

## ADDED Requirements

### Requirement: Generate a blind labels template
`deriva --labels-template <dictionary_A> <dictionary_B>` SHALL write
`labels_<A>_vs_<B>.csv` to the current directory with the columns `variable`,
`description_<A>`, `description_<B>`, `label` and `note`, and one row for every variable
present in both rounds whose descriptions are not identical strings. `label` and `note`
SHALL be empty. In this mode deriva SHALL NOT write the changes CSV and SHALL NOT print
or write any cosmetic/real classification; it SHALL print only the variable counts, the
added and removed counts, the number of rows written and the template path.

#### Scenario: Template on the real files
- **WHEN** `deriva --labels-template` is run on the 2021 and 2025 persona dictionaries in `data/`
- **THEN** `labels_2021_vs_2025.csv` has 22 rows with both descriptions filled in and empty `label` and `note` columns

#### Scenario: No verdict leaks
- **WHEN** the template is generated
- **THEN** neither the printed output nor any file written contains the words `cosmetic` or `real` as a classification of a variable

### Requirement: Never overwrite a labels file
deriva SHALL refuse to write the labels template when a file of that name already exists
in the current directory, exiting with a non-zero status and a message naming the file,
so labels already entered are never lost.

#### Scenario: Template already exists
- **WHEN** `labels_2021_vs_2025.csv` already exists and `deriva --labels-template` is run on the same rounds
- **THEN** the existing file is left unchanged and deriva exits with a non-zero status naming it

### Requirement: Evaluate labels against the rule
`deriva-eval <labels.csv>` SHALL read a labels file in the template format, apply the
same classification rule as deriva to the two descriptions in each row, and compare it
with the `label` column. Labels SHALL be `cosmetic` or `real`, read case-insensitively
and ignoring surrounding whitespace; an empty label SHALL mean the row is not labelled
yet. The evaluation SHALL need only the labels file, not the dictionaries.

#### Scenario: Invalid label
- **WHEN** a row's label is `maybe`
- **THEN** deriva-eval exits with a non-zero status and an error naming the variable and the invalid label

### Requirement: Report agreement and every disagreement
deriva-eval SHALL print how many rows are labelled out of the total, a 2×2 table of
hand label against rule verdict, the number and share of labelled rows where they agree,
and a list of every disagreement with the variable, the hand label, the rule verdict,
both descriptions and the note. It SHALL exit with status 0 when the evaluation completes.

#### Scenario: Partly labelled file
- **WHEN** 10 of 22 rows are labelled, 8 agree with the rule and 2 do not
- **THEN** deriva-eval reports 10 of 22 labelled, agreement 8 of 10, the 2×2 table over the 10 labelled rows, and lists the 2 disagreements

#### Scenario: Hand says real, rule says cosmetic
- **WHEN** a row labelled `real` has descriptions the rule classifies as cosmetic
- **THEN** that row appears in the disagreement list with both descriptions shown

### Requirement: Empty template is a valid input
deriva-eval SHALL accept a labels file with no labels filled in, report that 0 of N rows
are labelled and that there is nothing to measure yet, and exit with status 0.

#### Scenario: Freshly generated template
- **WHEN** deriva-eval is run on a template with 22 rows and no labels
- **THEN** it prints that 0 of 22 rows are labelled and there is nothing to measure yet, and exits with status 0
