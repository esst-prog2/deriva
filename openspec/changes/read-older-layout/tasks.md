## 1. Reader

- [x] 1.1 Recognise the older header (`CODIGO DE LA VARIABLE` and `PREGUNTA` in the same row, any columns) and read name and description from those columns
- [x] 1.2 Keep the 2021+ layout unchanged; name both headers in the "no header row found" error
- [x] 1.3 Tests with small invented workbooks: older layout read, `NOMBRE DE LA VARIABLE` ignored, header in other columns, near-miss header rejected, existing tests still pass
- [x] 1.4 Acceptance: the real 2019-12 and 2020-09 persona dictionaries read with 155 and 97 variables

## 2. Use

- [x] 2.1 Generate the blind labels template for 2019-12 vs 2020-09 with `deriva --labels-template`, without running plain `deriva` on that pair
- [x] 2.2 README: note the older layout and that comparing it with a 2021+ round is not meaningful
