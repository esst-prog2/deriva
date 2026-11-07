# dictionary-reader Specification

## Purpose

Reads one ENEMDU variable dictionary workbook, as INEC publishes it, into the list of
variable names and their descriptions, failing loudly when the layout is not recognised.

## Requirements

### Requirement: Locate the header row by its label
The reader SHALL locate the header row by finding a cell in the first column whose
trimmed text is exactly `Nombre del campo`, at any row of the sheet, or else the older
layout's header described in "Read INEC's older dictionary layout". Rows above the
header SHALL be ignored. A cell whose text merely starts with or resembles a label
SHALL NOT be taken as the header.

#### Scenario: Header below metadata rows
- **WHEN** the sheet has five rows of metadata and `Nombre del campo` in row 6
- **THEN** the variables are read from row 7 onwards and no metadata row is returned as a variable

#### Scenario: Header at a different row
- **WHEN** a sheet has `Nombre del campo` in row 2 instead of row 6
- **THEN** the variables are read from row 3 onwards

#### Scenario: Header with surrounding whitespace
- **WHEN** the first-column cell reads `  Nombre del campo ` with spaces around the label
- **THEN** it is taken as the header and the variables below it are read

#### Scenario: Header missing
- **WHEN** no cell in the first column reads exactly `Nombre del campo` and no row has both `CODIGO DE LA VARIABLE` and `PREGUNTA`
- **THEN** deriva exits with a non-zero status and an error message that names the file and both header texts it looked for

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

### Requirement: Reject a dictionary with no variables
The reader SHALL stop with an error naming the file when the header is found but no
variable follows it, rather than return an empty dictionary that would report every
variable of the other round as added or removed.

#### Scenario: Header without variables
- **WHEN** the sheet has `Nombre del campo` and only empty rows below it
- **THEN** deriva exits with a non-zero status and an error message naming the file

### Requirement: Read names and descriptions from the first two columns
Below the header, the reader SHALL take the variable name from the first column and its
description from the second column, and SHALL ignore every other column. Names SHALL be
trimmed of surrounding whitespace. A description cell that is empty SHALL be read as an
empty description. Descriptions SHALL otherwise be kept exactly as written.

#### Scenario: Extra empty columns
- **WHEN** the sheet has four columns, the last two empty
- **THEN** the result is the same as for the same data in a two-column sheet

#### Scenario: Description kept verbatim
- **WHEN** a description contains accents, capitals and doubled spaces
- **THEN** the description is returned with those characters unchanged

### Requirement: Skip empty rows
The reader SHALL skip every row below the header whose first two cells are both empty,
wherever it occurs, and SHALL continue reading after it.

#### Scenario: Trailing empty rows
- **WHEN** eleven empty rows follow the last variable
- **THEN** they produce no variables and no error

#### Scenario: Empty row between variables
- **WHEN** an empty row sits between two variables
- **THEN** both variables are read

### Requirement: Reject a description without a name
The reader SHALL stop with an error when a row below the header has a description but
an empty variable name, naming the file and the row number.

#### Scenario: Description without a name
- **WHEN** a row below the header has an empty first cell and `Area` in the second
- **THEN** deriva exits with a non-zero status and an error message naming the file and that row

### Requirement: Reject duplicate variable names
The reader SHALL stop with an error when the same variable name appears more than once
in one dictionary, naming the file and the duplicated variable.

#### Scenario: Duplicate name
- **WHEN** the variable `p54a` appears in two rows of the same sheet
- **THEN** deriva exits with a non-zero status and an error message naming the file and `p54a`

### Requirement: Read the first sheet of an xlsx workbook
The reader SHALL read the first worksheet of an `.xlsx` workbook. A path that does not
exist or cannot be opened as an `.xlsx` workbook SHALL produce an error naming the path.
So SHALL a workbook whose first sheet is corrupt and a workbook with no ordinary
worksheet, such as one holding only a chart sheet.

#### Scenario: Several sheets
- **WHEN** a workbook has two sheets and the second one is the active sheet
- **THEN** the variables are read from the first sheet only

#### Scenario: Missing file
- **WHEN** a path given to deriva does not exist
- **THEN** deriva exits with a non-zero status and an error message naming that path

#### Scenario: Corrupt sheet
- **WHEN** the workbook opens but its first sheet's XML is cut off, as in a download cut short
- **THEN** deriva exits with a non-zero status and an error message naming the file

#### Scenario: No ordinary worksheet
- **WHEN** the workbook holds only a chart sheet
- **THEN** deriva exits with a non-zero status and an error message naming the file

### Requirement: Real 2021 and 2025 dictionaries read correctly
The reader SHALL read the 2021 and 2025 ENEMDU annual persona dictionaries in `data/`
with the counts checked against the files by hand.

#### Scenario: Variable counts on the real files
- **WHEN** the 2021 and 2025 persona dictionaries in `data/` are read
- **THEN** the 2021 dictionary yields 151 variables and the 2025 dictionary yields 139 variables
