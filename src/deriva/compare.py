"""Lining two rounds up by variable name and classifying what changed."""

from dataclasses import dataclass

from deriva.reader import Dictionary
from deriva.rule import COSMETIC, REAL, UNCHANGED, classify

ADDED = "added"
REMOVED = "removed"


@dataclass
class Alignment:
    """Two rounds lined up by exact variable name, before any classification."""

    a: Dictionary
    b: Dictionary
    added: list[str]  # only in b, in b's sheet order
    removed: list[str]  # only in a, in a's sheet order
    differing: list[str]  # in both, descriptions not identical strings, in a's order
    unchanged: list[str]  # in both, descriptions identical


@dataclass
class Change:
    variable: str
    change: str  # added, removed, cosmetic or real
    description_a: str
    description_b: str


def align(a: Dictionary, b: Dictionary) -> Alignment:
    shared = [name for name in a.variables if name in b.variables]
    return Alignment(
        a=a,
        b=b,
        added=[name for name in b.variables if name not in a.variables],
        removed=[name for name in a.variables if name not in b.variables],
        differing=[n for n in shared if a.variables[n] != b.variables[n]],
        unchanged=[n for n in shared if a.variables[n] == b.variables[n]],
    )


def classify_changes(alignment: Alignment) -> list[Change]:
    """Every change, real ones first, then cosmetic, removed and added."""
    a, b = alignment.a.variables, alignment.b.variables
    verdicts = {name: classify(a[name], b[name]) for name in alignment.differing}
    assert UNCHANGED not in verdicts.values()  # differing means not identical strings
    return (
        [Change(n, REAL, a[n], b[n]) for n in alignment.differing if verdicts[n] == REAL]
        + [Change(n, COSMETIC, a[n], b[n]) for n in alignment.differing if verdicts[n] == COSMETIC]
        + [Change(n, REMOVED, a[n], "") for n in alignment.removed]
        + [Change(n, ADDED, "", b[n]) for n in alignment.added]
    )
