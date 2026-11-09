## ADDED Requirements

### Requirement: Variable history across rounds
`deriva-history <folder>` SHALL read every persona dictionary in the folder, in either
layout, order the rounds by date taken from the file name, and write
`deriva_history.html` to the current directory: a single self-contained page that lists,
for each variable, its description in every round where it appears. Between two
consecutive rounds of the same layout, each change SHALL be marked cosmetic or real by
the second rule. Between the last pre-2021 round and the first 2021+ round, the page
SHALL show a layout break and SHALL NOT mark any change.

#### Scenario: A real change in the history
- **WHEN** `deriva-history data/` is run on the nine persona dictionaries from 2019-06 to 2025
- **THEN** the timeline for `p76` marks December 2020 as a real change from "BONO DE DESARROLLO HUMANO" to "BONO o PENSIÓN"

#### Scenario: Layout break
- **WHEN** a variable appears in both 2020-12 and 2021
- **THEN** its timeline shows the redesign between them as a break, not as a change
