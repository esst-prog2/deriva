## ADDED Requirements

### Requirement: Read INEC's older dictionary layout
The reader SHALL also accept INEC's older dictionary layout, used before 2021: a header
row containing, in any columns, a cell whose trimmed text is exactly
`CODIGO DE LA VARIABLE` and a cell whose trimmed text is exactly `PREGUNTA`. Rows above
that header SHALL be ignored. Below it, the variable name SHALL be read from the
`CODIGO DE LA VARIABLE` column and the description from the `PREGUNTA` column; every
other column, including `NOMBRE DE LA VARIABLE`, SHALL be ignored. All other reader
requirements (trimmed names, verbatim descriptions, skipped empty rows, errors for a
description without a name, duplicate names and no variables) SHALL apply to this
layout as to the 2021+ layout.

#### Scenario: Older layout
- **WHEN** a sheet has metadata rows, then a header row with `CODIGO DE LA VARIABLE`, `NOMBRE DE LA VARIABLE` and `PREGUNTA` starting in column C, then variable rows
- **THEN** each variable is read with its `CODIGO DE LA VARIABLE` value as the name and its `PREGUNTA` value as the description

#### Scenario: Older layout on the real files
- **WHEN** the 2019-12 and 2020-09 persona dictionaries in `data/` are read
- **THEN** they yield 155 and 97 variables

#### Scenario: Older header without a question column
- **WHEN** a row has `CODIGO DE LA VARIABLE` but no `PREGUNTA` cell, and no `Nombre del campo` header exists
- **THEN** deriva exits with a non-zero status and an error naming the file and both headers it looked for

## MODIFIED Requirements

### Requirement: Locate the header row by its label
The reader SHALL locate the header row by finding a cell in the first column whose
trimmed text is exactly `Nombre del campo`, at any row of the sheet, or else the older
layout's header described in "Read INEC's older dictionary layout". Rows above the
header SHALL be ignored. A cell whose text merely starts with or resembles a label
SHALL NOT be taken as the header.

#### Scenario: Header missing
- **WHEN** no cell in the first column reads exactly `Nombre del campo` and no row has both `CODIGO DE LA VARIABLE` and `PREGUNTA`
- **THEN** deriva exits with a non-zero status and an error message that names the file and both header texts it looked for
