"""The `deriva` command."""

import argparse
import sys
from dataclasses import replace
from pathlib import Path

from deriva import DerivaError
from deriva.compare import align, classify_changes
from deriva.output import summary, template_summary, write_changes, write_labels_template
from deriva.reader import distinct_labels, read_dictionary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deriva",
        description="Compare the variable dictionaries of two survey rounds and report what changed.",
    )
    parser.add_argument("dictionary_a", help="dictionary of the earlier round (.xlsx)")
    parser.add_argument("dictionary_b", help="dictionary of the later round (.xlsx)")
    parser.add_argument(
        "--labels-template",
        action="store_true",
        help="write a blind labels template instead of the changes CSV; "
        "prints no cosmetic/real verdicts",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        a = read_dictionary(args.dictionary_a)
        b = read_dictionary(args.dictionary_b)
        label_a, label_b = distinct_labels(a.label, b.label)
        alignment = align(replace(a, label=label_a), replace(b, label=label_b))

        if args.labels_template:
            path = write_labels_template(alignment, Path.cwd())
            print(template_summary(alignment, path))
        else:
            changes = classify_changes(alignment)
            path = write_changes(changes, alignment, Path.cwd())
            print(summary(alignment, changes, path))
    except DerivaError as error:
        print(f"deriva: error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
