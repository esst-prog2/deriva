## ADDED Requirements

### Requirement: Evaluate an optional second rule
`deriva-eval <labels.csv> --rule v2` SHALL evaluate the labels against a second rule
instead of deriva's rule. The second rule SHALL classify as cosmetic everything the first
rule classifies as cosmetic, and also a pair of descriptions that become identical after
the first rule's normalisation when (a) any Spanish month name is treated as the same
word, (b) the variable's own name at the start of a description, followed by
punctuation or a space, is removed, and (c) a number followed by an ordinal suffix such
as `er`, `vo` or `to` is treated as the number alone. The report SHALL start with the
line `rule: v2`. `--rule v1`, the default, SHALL give exactly the report of the first
rule. deriva's own classification SHALL NOT change.

#### Scenario: Reference month
- **WHEN** a row labelled cosmetic has `En el mes de NOVIEMBRE` and `En el mes de MAYO`
- **THEN** `--rule v2` counts it as agreeing and the default rule counts it as a disagreement

#### Scenario: Different number
- **WHEN** the descriptions are `Recibe 13er sueldo` and `Recibe 14vo sueldo`
- **THEN** the second rule classifies them as real

#### Scenario: Unknown rule
- **WHEN** deriva-eval is run with `--rule v3`
- **THEN** it exits with a non-zero status and prints its usage
