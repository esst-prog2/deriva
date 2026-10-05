# Spec Delta

## Purpose

The `deriva` command: compares the variable dictionaries of two survey rounds and reports
which variables were added or removed and which descriptions changed, cosmetically or
really.

## ADDED Requirements

### Requirement: Command takes two dictionary files
deriva SHALL be run as `deriva <dictionary_A> <dictionary_B>`, where A is the earlier
round and B the later one. Each round SHALL be labelled by the last four-digit year
(19xx or 20xx) in its file name, or by the file name without extension when it contains
no such year. When both files yield the same label, the rounds SHALL be labelled
`<label>_a` and `<label>_b`.

#### Scenario: Same label twice
- **WHEN** deriva is run with the same 2021 file as A and B
- **THEN** the rounds are labelled `2021_a` and `2021_b`

#### Scenario: Round labels from file names
- **WHEN** deriva is run on `Diccionario de Datos_persona_anual_2021.xlsx` and `Diccionario de Datos_persona_anual_2025.xlsx`
- **THEN** the rounds are labelled `2021` and `2025` in the summary and the output file names

#### Scenario: Wrong number of arguments
- **WHEN** deriva is run with one file or with three
- **THEN** it exits with a non-zero status and prints its usage

### Requirement: Align rounds by variable name
deriva SHALL match variables between the two rounds by exact name. A name only in A
SHALL be reported as `removed`; a name only in B SHALL be reported as `added`. Names
differing only in case SHALL be treated as different variables.

#### Scenario: Removed variable
- **WHEN** `p54a` is in A and not in B
- **THEN** `p54a` is reported as removed

#### Scenario: Added variable
- **WHEN** `p99` is in B and not in A
- **THEN** `p99` is reported as added

### Requirement: Classify description changes
For each variable in both rounds deriva SHALL classify the description as:
- `unchanged` when the two descriptions are identical strings;
- `cosmetic` when they differ but become identical after normalising both: removing
  accents, ignoring case, treating punctuation as whitespace and collapsing runs of
  whitespace;
- `real` when they still differ after normalising.

#### Scenario: Accent only
- **WHEN** the descriptions are `Area` and `Área`
- **THEN** the variable is classified as cosmetic

#### Scenario: Capitalisation only
- **WHEN** the descriptions are `Rama de actividad` and `rama de Actividad`
- **THEN** the variable is classified as cosmetic

#### Scenario: Punctuation and spacing only
- **WHEN** the descriptions are `Ingreso  total.` and `Ingreso total`
- **THEN** the variable is classified as cosmetic

#### Scenario: Words changed
- **WHEN** the descriptions are `Rama de actividad CIIU4` and `Rama de actividad CIIU 4.1`
- **THEN** the variable is classified as real

#### Scenario: Words removed
- **WHEN** the descriptions are `Horas en el trabajo secundario` and `Horas en el`
- **THEN** the variable is classified as real

### Requirement: Print a summary
deriva SHALL print the number of variables in each round and the number of variables
added, removed, cosmetically changed and really changed, followed by the path of the
changes CSV it wrote. deriva SHALL exit with status 0 whenever the comparison completes,
whether or not changes were found.

#### Scenario: Summary on the real files
- **WHEN** deriva is run on the 2021 and 2025 persona dictionaries in `data/`
- **THEN** it reports 151 variables in 2021, 139 in 2025, 12 removed, 0 added, and cosmetic plus real changes totalling 22, and exits with status 0

#### Scenario: Dictionary against itself
- **WHEN** deriva is run with the same dictionary file as both A and B
- **THEN** it reports 0 added, 0 removed, 0 cosmetic and 0 real changes

### Requirement: Write a changes CSV
deriva SHALL write `deriva_<A>_vs_<B>.csv` to the current directory, replacing any
existing file of that name, with the columns `variable`, `change`, `description_<A>`,
`description_<B>` and `reason`, and one row per variable that was added, removed,
cosmetically changed or really changed. Unchanged variables SHALL NOT appear. For an
added variable the A description SHALL be empty; for a removed variable the B description
SHALL be empty. `reason` SHALL state in words why the row was classified as it was. The
file SHALL be UTF-8 encoded and open with accents intact in Excel.

#### Scenario: Real change row
- **WHEN** a variable's description changes from `Rama de actividad CIIU4` to `Rama de actividad CIIU 4.1`
- **THEN** its row has `change` = `real`, both descriptions in full, and a reason stating the descriptions still differ after normalising accents, case, punctuation and whitespace

#### Scenario: No changes
- **WHEN** a dictionary is compared with itself
- **THEN** the CSV contains only the header row
