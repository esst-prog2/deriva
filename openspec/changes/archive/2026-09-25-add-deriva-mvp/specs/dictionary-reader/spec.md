# Spec Delta

## Purpose

Reads one ENEMDU variable dictionary workbook, as INEC publishes it, into the list of
variable names and their descriptions, failing loudly when the layout is not recognised.

## ADDED Requirements

### Requirement: Locate the header row by its label
The reader SHALL locate the header row by finding a cell in the first column whose
trimmed text is exactly `Nombre del campo`, at any row of the sheet. Rows above the
header SHALL be ignored. A cell whose text merely starts with or resembles the label
SHALL NOT be taken as the header.

#### Scenario: Header below metadata rows
- **WHEN** the sheet has five rows of metadata and `Nombre del campo` in row 6
- **THEN** the variables are read from row 7 onwards and no metadata row is returned as a variable

#### Scenario: Header at a different row
- **WHEN** a sheet has `Nombre del campo` in row 2 instead of row 6
- **THEN** the variables are read from row 3 onwards

#### Scenario: Header missing
- **WHEN** no cell in the first column reads exactly `Nombre del campo`
- **THEN** deriva exits with a non-zero status and an error message that names the file and the header text `Nombre del campo` it looked for and did not find

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

### Requirement: Reject duplicate variable names
The reader SHALL stop with an error when the same variable name appears more than once
in one dictionary, naming the file and the duplicated variable.

#### Scenario: Duplicate name
- **WHEN** the variable `p54a` appears in two rows of the same sheet
- **THEN** deriva exits with a non-zero status and an error message naming the file and `p54a`

### Requirement: Read the first sheet of an xlsx workbook
The reader SHALL read the first worksheet of an `.xlsx` workbook. A path that does not
exist or cannot be opened as an `.xlsx` workbook SHALL produce an error naming the path.

#### Scenario: Missing file
- **WHEN** a path given to deriva does not exist
- **THEN** deriva exits with a non-zero status and an error message naming that path

### Requirement: Real 2021 and 2025 dictionaries read correctly
The reader SHALL read the 2021 and 2025 ENEMDU annual persona dictionaries in `data/`
with the counts checked against the files by hand.

#### Scenario: Variable counts on the real files
- **WHEN** the 2021 and 2025 persona dictionaries in `data/` are read
- **THEN** the 2021 dictionary yields 151 variables and the 2025 dictionary yields 139 variables
