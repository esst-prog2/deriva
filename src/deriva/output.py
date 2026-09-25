"""The changes CSV, the labels template and the printed summary."""

import csv
from collections import Counter
from pathlib import Path

from deriva import DerivaError
from deriva.compare import ADDED, REMOVED, Alignment, Change
from deriva.rule import COSMETIC, REAL

# utf-8-sig writes a byte-order mark so Excel opens the file with accents intact.
ENCODING = "utf-8-sig"
NORMALISED = "accents, case, punctuation and whitespace"


def reason(change: Change, label_a: str, label_b: str) -> str:
    if change.change == ADDED:
        return f"only in {label_b}"
    if change.change == REMOVED:
        return f"only in {label_a}"
    if change.change == COSMETIC:
        return f"descriptions differ, but are identical after normalising {NORMALISED}"
    return f"descriptions still differ after normalising {NORMALISED}"


def write_changes(changes: list[Change], alignment: Alignment, directory: Path) -> Path:
    label_a, label_b = alignment.a.label, alignment.b.label
    path = directory / f"deriva_{label_a}_vs_{label_b}.csv"
    with path.open("w", encoding=ENCODING, newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["variable", "change", f"description_{label_a}", f"description_{label_b}", "reason"]
        )
        for change in changes:
            writer.writerow(
                [
                    change.variable,
                    change.change,
                    change.description_a,
                    change.description_b,
                    reason(change, label_a, label_b),
                ]
            )
    return path


def write_labels_template(alignment: Alignment, directory: Path) -> Path:
    """Write the pairs to label, with no verdict. Never overwrites an existing file."""
    label_a, label_b = alignment.a.label, alignment.b.label
    a, b = alignment.a.variables, alignment.b.variables
    path = directory / f"labels_{label_a}_vs_{label_b}.csv"
    try:
        f = path.open("x", encoding=ENCODING, newline="")
    except FileExistsError:
        raise DerivaError(
            f"{path.name} already exists; not overwriting it, so no labels are lost. "
            "Move or rename it to generate a fresh template."
        ) from None
    with f:
        writer = csv.writer(f)
        writer.writerow(["variable", f"description_{label_a}", f"description_{label_b}", "label", "note"])
        for name in alignment.differing:
            writer.writerow([name, a[name], b[name], "", ""])
    return path


def _variable_counts(alignment: Alignment) -> list[str]:
    return [
        f"{alignment.a.label}: {len(alignment.a.variables)} variables",
        f"{alignment.b.label}: {len(alignment.b.variables)} variables",
        "",
        f"  added      {len(alignment.added):>4}",
        f"  removed    {len(alignment.removed):>4}",
    ]


def summary(alignment: Alignment, changes: list[Change], path: Path) -> str:
    counts = Counter(change.change for change in changes)
    return "\n".join(
        _variable_counts(alignment)
        + [
            f"  cosmetic   {counts[COSMETIC]:>4}",
            f"  real       {counts[REAL]:>4}",
            f"  unchanged  {len(alignment.unchanged):>4}",
            "",
            f"wrote {path}",
        ]
    )


def template_summary(alignment: Alignment, path: Path) -> str:
    return "\n".join(
        _variable_counts(alignment)
        + [
            f"  descriptions differing {len(alignment.differing):>4}  (not classified, so labelling stays blind)",
            "",
            f"wrote {path} with {len(alignment.differing)} rows to label",
        ]
    )
