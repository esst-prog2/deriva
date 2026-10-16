# classifier-evaluation Specification

## Purpose

Measures how often deriva's cosmetic-vs-real rule agrees with a person's hand labels,
using a blind labelling template and an agreement report that lists every disagreement.

## Requirements

### Requirement: Generate a blind labels template
`deriva --labels-template <dictionary_A> <dictionary_B>` SHALL write
`labels_<A>_vs_<B>.csv` to the current directory with the columns `variable`,
`description_<A>`, `description_<B>`, `label` and `note`, and one row for every variable
present in both rounds whose descriptions are not identical strings. `label` and `note`
SHALL be empty. In this mode deriva SHALL NOT write the changes CSV and SHALL NOT print
or write any cosmetic/real classification; it SHALL print only the variable counts, the
added and removed counts, the number of variables whose descriptions differ, the number
of rows written and the template path.

#### Scenario: Template on the real files
- **WHEN** `deriva --labels-template` is run on the 2021 and 2025 persona dictionaries in `data/`
- **THEN** `labels_2021_vs_2025.csv` has 22 rows with both descriptions filled in and empty `label` and `note` columns

#### Scenario: Both descriptions copied into the template
- **WHEN** a variable's description changes from `Area` to `Área` and another from `Rama CIIU4` to `Rama CIIU 4.1`
- **THEN** each template row holds the variable, its A description and its B description exactly as read, and nothing else is filled in

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

### Requirement: Accept a labels file re-saved by a spreadsheet
deriva-eval SHALL accept a labels file whose columns are separated by `,` or by `;`, as
Excel in a Spanish locale saves CSV. It SHALL find the columns by their header names,
so the columns MAY appear in any order and extra columns SHALL be ignored. The header
SHALL contain `variable`, `label`, `note` and exactly two columns whose names start with
`description_`; the text after `description_` names each round in the report. The
first `description_` column in the header SHALL be treated as round A and the second as
round B, whatever their names.

#### Scenario: Description columns in reverse order
- **WHEN** the header has `description_2025` before `description_2021`
- **THEN** deriva-eval treats 2025 as round A and shows its description first in each disagreement

#### Scenario: Semicolon-separated file
- **WHEN** the labels file uses `;` between columns
- **THEN** deriva-eval reads it as it would the same file with `,`

#### Scenario: Columns reordered and an extra column
- **WHEN** the columns are in the order `label`, `variable`, `note`, `description_2025`, `description_2021`, `extra`
- **THEN** deriva-eval reads the rows correctly and ignores `extra`

### Requirement: Reject an unusable labels file
deriva-eval SHALL exit with a non-zero status and an error naming the file when the file
is empty, when its header does not have the columns above, or when a row's two
descriptions are identical strings, since such a row has no change to label; that error
SHALL also name the variable.

#### Scenario: Empty file
- **WHEN** the labels file is empty
- **THEN** deriva-eval exits with a non-zero status and an error saying the file is empty

#### Scenario: Wrong columns
- **WHEN** the header is `name,description`
- **THEN** deriva-eval exits with a non-zero status and an error listing the expected columns

#### Scenario: Identical descriptions
- **WHEN** a row's two descriptions are both `Area`
- **THEN** deriva-eval exits with a non-zero status and an error naming that variable

### Requirement: Report errors on stderr
When deriva-eval stops with an error, it SHALL print one message to stderr starting with
`deriva-eval: error: ` and SHALL exit with status 1.

#### Scenario: Error message format
- **WHEN** a row's label is `maybe`
- **THEN** stderr starts with `deriva-eval: error: ` and the exit status is 1

### Requirement: Report agreement and every disagreement
deriva-eval SHALL print how many rows are labelled out of the total, a 2×2 table of
hand label against rule verdict, the number and share of labelled rows where they agree,
and a list of every disagreement with the variable, the hand label, the rule verdict,
both descriptions and the note. Disagreements where the hand label is `real` and the rule
says `cosmetic` SHALL be listed first, since those are real changes the rule would hide.
It SHALL exit with status 0 when the evaluation completes.

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
