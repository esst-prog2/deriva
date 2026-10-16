# Code review (Homework 6)

Whole-repository review of deriva, one kind of problem at a time.
Each section lists what I looked for, what I found, and what I did about it.
Each review is its own commit on the `hw6-review` branch.

## 1. Spec drift

**Looked for:** code that does something no spec requirement describes, and spec
requirements that the code does not build or that no test checks.

**Found:**
- "Punctuation" was not defined. The rule uses Unicode punctuation categories, so `%`
  and `/` are dropped while `>=`, `$` and `°` are kept.
- The labels template prints a "descriptions differing" line the spec did not allow.
- Several behaviours existed only in the code: `,` or `;` delimiter in deriva-eval,
  input errors, disagreement order, row order in the changes CSV, the unchanged count,
  and the error for a description without a name.
- Some requirements had no test.

**Did:**
- Did not change the rule, because the 12 of 22 measurement depends on it. Wrote the
  existing behaviour into the specs instead, with new scenarios.
- Added the missing tests with small invented inputs, not the real files.
- No code in `src/` changed. Specs pass `openspec validate --specs --strict`.

**Left open:** accent removal also folds `ñ` to `n`, so `Año` vs `Ano` counts as
cosmetic. In Spanish these are different words, so this could hide a real change.
Logged, not changed yet.