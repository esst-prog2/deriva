"""The `deriva-eval` command: how often the rule agrees with hand labels."""

import argparse
import csv
import io
import sys
from dataclasses import dataclass
from pathlib import Path

from deriva import DerivaError
from deriva.output import ENCODING
from deriva.rule import COSMETIC, REAL, UNCHANGED, classify

LABELS = (COSMETIC, REAL)
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


def read_labels(path: Path) -> LabelsFile:
    try:
        text = path.read_text(encoding=ENCODING)
    except OSError as exc:
        raise DerivaError(f"{path}: cannot be read ({exc.strerror})") from exc

    if not text.strip():
        raise DerivaError(f"{path}: file is empty")
    for delimiter in DELIMITERS:
        header = next(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter))
        descriptions = [c for c in header if c.startswith("description_")]
        if {"variable", "label", "note"} <= set(header) and len(descriptions) == 2:
            break
    else:
        raise DerivaError(
            f"{path}: expected the columns variable, two description_<round> columns, "
            "label and note, separated by , or ;"
        )

    rows = []
    for record in csv.DictReader(io.StringIO(text, newline=""), delimiter=delimiter):
        variable = (record["variable"] or "").strip()
        a, b = record[descriptions[0]] or "", record[descriptions[1]] or ""
        verdict = classify(a, b)
        if verdict == UNCHANGED:
            raise DerivaError(f"{path}: {variable!r} has identical descriptions, so there is nothing to label")
        rows.append(
            Row(
                variable=variable,
                description_a=a,
                description_b=b,
                label=_parse_label(path, variable, record["label"]),
                note=(record["note"] or "").strip(),
                verdict=verdict,
            )
        )
    return LabelsFile(
        label_a=descriptions[0].removeprefix("description_"),
        label_b=descriptions[1].removeprefix("description_"),
        rows=rows,
    )


def _parse_label(path: Path, variable: str, raw: str | None) -> str | None:
    label = (raw or "").strip().casefold()
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
    args = parser.parse_args(argv)
    path = Path(args.labels_csv)
    try:
        print(report(path, read_labels(path)))
    except DerivaError as error:
        print(f"deriva-eval: error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
