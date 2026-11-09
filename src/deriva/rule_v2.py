"""An optional second cosmetic/real rule, built from the two labelled pairs.

It starts from the first rule's normalisation (rule.normalise) and also treats three
patterns as cosmetic, each one I labelled cosmetic by hand:
- a different reference month, such as "en el mes de NOVIEMBRE" vs "en el mes de MAYO";
- the variable's own code repeated at the start of the text, such as "CED01A. ...";
- an abbreviated ordinal with a different suffix, such as "13er" vs "13vo".

It was built after seeing the 2021 vs 2025 and 2019-12 vs 2020-09 labels, so it may
only be measured on a pair of rounds that was not looked at. The first rule is unchanged.
"""

import re

from deriva.rule import COSMETIC, REAL, UNCHANGED, normalise

MONTHS = (
    "enero febrero marzo abril mayo junio julio agosto septiembre setiembre octubre noviembre diciembre"
).split()
MONTH = re.compile(r"\b(?:" + "|".join(MONTHS) + r")\b")
ORDINAL = re.compile(r"\b(\d+)(?:er|ero|ra|do|da|vo|va|to|ta|mo|ma|no|na)\b")


def normalise_v2(text: str, variable: str = "") -> str:
    """The first rule's normalisation, plus the three patterns above."""
    text = normalise(text)
    code = normalise(variable)
    if code and text.startswith(code + " "):
        text = text[len(code) + 1 :]
    text = MONTH.sub("<month>", text)
    return ORDINAL.sub(r"\1", text)


def classify_v2(description_a: str, description_b: str, variable: str = "") -> str:
    """Classify the change from description_a to description_b with the second rule."""
    if description_a == description_b:
        return UNCHANGED
    if normalise_v2(description_a, variable) == normalise_v2(description_b, variable):
        return COSMETIC
    return REAL
