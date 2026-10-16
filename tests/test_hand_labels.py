"""The rule must not call cosmetic a change the user judged real by hand.

The expected labels come from the user's blind hand labels in
eval/labels_2021_vs_2025.csv, made before seeing the rule's verdicts, not from the rule.
"""

from pathlib import Path

import pytest

from deriva.evaluate import read_labels
from deriva.rule import REAL, classify

LABELS_CSV = Path(__file__).resolve().parent.parent / "eval" / "labels_2021_vs_2025.csv"
HAND_REAL = ("p54a", "p77", "rama1")


def hand_labels():
    """Read the way deriva-eval reads it, so both see the same labels."""
    return {row.variable: row for row in read_labels(LABELS_CSV).rows}


def test_the_three_are_the_hand_real_rows():
    real = {v for v, row in hand_labels().items() if row.label == REAL}
    assert real == set(HAND_REAL)


@pytest.mark.parametrize("variable", HAND_REAL)
def test_rule_agrees_with_hand_label(variable):
    row = hand_labels()[variable]
    assert classify(row.description_a, row.description_b) == row.label
