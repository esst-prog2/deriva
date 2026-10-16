"""The rule that separates cosmetic description changes from real ones.

Two descriptions that differ only in accents, case, punctuation or whitespace are a
cosmetic change; anything that survives normalisation is a real change. The rule is a
judgement and will misfile some cases, which is why deriva-eval exists.

Each term is defined by Unicode, as in the round-comparison spec:
- accents: NFKD, then every combining mark (category Mn) is dropped. NFKD also folds
  compatibility characters, so m² becomes m2, and ñ becomes n;
- case: casefold, so ß matches ss;
- punctuation: every character in a P* category (such as . , % /) becomes a space;
  symbols in S* categories (such as $ ° > =) are kept;
- whitespace: runs collapse to one space, leading and trailing space is dropped.
"""

import unicodedata

UNCHANGED = "unchanged"
COSMETIC = "cosmetic"
REAL = "real"

# What normalise() makes no difference to, in the words the changes CSV uses.
NORMALISED = "accents, case, punctuation and whitespace"


def normalise(text: str) -> str:
    """NFKD and drop Mn marks (m² -> m2, ñ -> n), casefold, turn P* punctuation into
    spaces, keep S* symbols, and collapse whitespace."""
    decomposed = unicodedata.normalize("NFKD", text)
    chars = []
    for ch in decomposed:
        category = unicodedata.category(ch)
        if category == "Mn":  # combining mark, e.g. the accent split off by NFKD
            continue
        # A space rather than nothing, so "CIIU 4.1" stays distinct from "CIIU4".
        chars.append(" " if category.startswith("P") else ch)
    return " ".join("".join(chars).casefold().split())


def classify(description_a: str, description_b: str) -> str:
    """Classify the change from description_a to description_b."""
    if description_a == description_b:
        return UNCHANGED
    if normalise(description_a) == normalise(description_b):
        return COSMETIC
    return REAL
