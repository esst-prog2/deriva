"""The `deriva-eval` command: how often the rule agrees with hand labels."""

import argparse
import csv
import io
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from deriva import DerivaError
from deriva.output import DESCRIPTION_PREFIX, ENCODING, LABEL_COLUMN, NOTE_COLUMN, VARIABLE_COLUMN
from deriva.rule import COSMETIC, REAL, UNCHANGED, classify
from deriva.rule_v2 import classify_v2

LABELS = (COSMETIC, REAL)
# v1 is the rule deriva uses; v2 is the optional second rule, measured only on unseen pairs.
RULES = {"v1": lambda a, b, variable: classify(a, b), "v2": classify_v2}
DELIMITERS = (",", ";")  # Excel in a Spanish locale saves CSV with ";"


@dataclass
class Row:
    variable: str
    description_a: str
    description_b: str
    label: str | None  # cosmetic, real, or None when not labelled yet
    note: str
    verdict: str  # what the rule says


@dataclass
class LabelsFile:
    label_a: str
    label_b: str
    rows: list[Row]


def read_labels(path: Path, rule: str = "v1") -> LabelsFile:
    try:
        text = path.read_text(encoding=ENCODING)
    except OSError as exc:
        raise DerivaError(f"{path}: cannot be read ({exc.strerror})") from exc
    except UnicodeDecodeError as exc:
        raise DerivaError(f'{path}: is not UTF-8 text; save it again as "CSV UTF-8"') from exc

    if not text.strip():
        raise DerivaError(f"{path}: file is empty")
    for delimiter in DELIMITERS:
        header = next(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter))
        descriptions = [c for c in header if c.startswith(DESCRIPTION_PREFIX)]
        if {VARIABLE_COLUMN, LABEL_COLUMN, NOTE_COLUMN} <= set(header) and len(descriptions) == 2:
            break
    else:
        raise DerivaError(
            f"{path}: expected the columns {VARIABLE_COLUMN}, two {DESCRIPTION_PREFIX}<round> columns, "
            f"{LABEL_COLUMN} and {NOTE_COLUMN}, separated by , or ;"
        )
    # Blank names are left alone: a spreadsheet can save empty trailing columns.
    repeated = [name for name, n in Counter(header).items() if n > 1 and name.strip()]
    if repeated:
        raise DerivaError(f"{path}: column {repeated[0]!r} appears more than once in the header")

    rows = []
    seen = set()
    for row_number, fields in _records(path, text, delimiter):
        if len(fields) != len(header):
            raise DerivaError(f"{path}: row {row_number} has {len(fields)} fields; the header has {len(header)}")
        record = dict(zip(header, fields))
        variable = record[VARIABLE_COLUMN].strip()
        if not variable:
            raise DerivaError(f"{path}: row {row_number} has no variable name")
        if variable in seen:
            raise DerivaError(f"{path}: variable {variable!r} appears more than once (again in row {row_number})")
        seen.add(variable)
        a, b = record[descriptions[0]], record[descriptions[1]]
        verdict = RULES[rule](a, b, variable)
        if verdict == UNCHANGED:
            raise DerivaError(f"{path}: {variable!r} has identical descriptions, so there is nothing to label")
        rows.append(
            Row(
                variable=variable,
                description_a=a,
                description_b=b,
                label=_parse_label(path, variable, record[LABEL_COLUMN]),
                note=record[NOTE_COLUMN].strip(),
                verdict=verdict,
            )
        )
    return LabelsFile(
        label_a=descriptions[0].removeprefix(DESCRIPTION_PREFIX),
        label_b=descriptions[1].removeprefix(DESCRIPTION_PREFIX),
        rows=rows,
    )


def _records(path: Path, text: str, delimiter: str):
    """(row number, fields) for each non-empty row below the header, numbered as a
    spreadsheet shows them: the header is row 1 and a multi-line cell is one row."""
    # strict, so an unclosed quote is an error instead of swallowing the rows after it.
    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True)
    row_number = 0
    try:
        for fields in reader:
            row_number += 1
            if row_number > 1 and fields:
                yield row_number, fields
    except csv.Error as exc:
        raise DerivaError(f"{path}: row {row_number + 1} cannot be read as CSV ({exc})") from exc


def _parse_label(path: Path, variable: str, raw: str) -> str | None:
    label = raw.strip().casefold()
    if not label:
        return None
    if label not in LABELS:
        raise DerivaError(
            f"{path}: {variable!r} has label {raw.strip()!r}; expected cosmetic, real or empty"
        )
    return label


def report(path: Path, labels: LabelsFile) -> str:
    labelled = [row for row in labels.rows if row.label is not None]
    lines = [f"{path.name}: {len(labelled)} of {len(labels.rows)} rows labelled"]
    if not labelled:
        return "\n".join(lines + ["nothing to measure yet"])

    def count(label, verdict):
        return sum(1 for row in labelled if row.label == label and row.verdict == verdict)

    agree = sum(1 for row in labelled if row.label == row.verdict)
    # Hand-real/rule-cosmetic first: those are real changes the rule would hide.
    disagreements = sorted(
        (row for row in labelled if row.label != row.verdict), key=lambda row: row.label != REAL
    )
    lines += [
        "",
        "                 rule: cosmetic  rule: real",
        f"  you: cosmetic  {count(COSMETIC, COSMETIC):>14}  {count(COSMETIC, REAL):>10}",
        f"  you: real      {count(REAL, COSMETIC):>14}  {count(REAL, REAL):>10}",
        "",
        f"agreement: {agree} of {len(labelled)} ({agree / len(labelled):.0%})",
        "",
        f"disagreements: {len(disagreements)}",
    ]
    for row in disagreements:
        lines += [
            "",
            f"  {row.variable}  you: {row.label}  rule: {row.verdict}",
            f"    {labels.label_a}: {row.description_a}",
            f"    {labels.label_b}: {row.description_b}",
        ]
        if row.note:
            lines.append(f"    note: {row.note}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="deriva-eval",
        description="Compare hand labels in a deriva labels file with deriva's cosmetic/real rule.",
    )
    parser.add_argument("labels_csv", help="labels file written by deriva --labels-template")
    parser.add_argument(
        "--rule",
        choices=sorted(RULES),
        default="v1",
        help="v1 is the rule deriva uses (default); v2 is the optional second rule",
    )
    args = parser.parse_args(argv)
    path = Path(args.labels_csv)
    try:
        text = report(path, read_labels(path, args.rule))
        print(text if args.rule == "v1" else f"rule: {args.rule}\n{text}")
    except DerivaError as error:
        print(f"deriva-eval: error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
