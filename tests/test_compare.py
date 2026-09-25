from deriva.compare import ADDED, REMOVED, align, classify_changes
from deriva.reader import Dictionary
from deriva.rule import COSMETIC, REAL


def dictionaries(a, b):
    return Dictionary("2021", a), Dictionary("2025", b)


def test_removed_and_added():
    alignment = align(*dictionaries({"p54a": "x", "area": "Area"}, {"area": "Area", "p99": "y"}))
    assert alignment.removed == ["p54a"]
    assert alignment.added == ["p99"]
    assert alignment.unchanged == ["area"]
    assert alignment.differing == []


def test_names_differing_in_case_are_different_variables():
    alignment = align(*dictionaries({"rama1": "Rama"}, {"RAMA1": "Rama"}))
    assert alignment.removed == ["rama1"]
    assert alignment.added == ["RAMA1"]


def test_classify_changes():
    a = {"area": "Area", "rama1": "Rama CIIU4", "p54a": "x", "ciudad": "Ciudad"}
    b = {"area": "Área", "rama1": "Rama CIIU 4.1", "ciudad": "Ciudad", "p99": "y"}
    changes = classify_changes(align(*dictionaries(a, b)))
    assert [(c.variable, c.change) for c in changes] == [
        ("rama1", REAL),
        ("area", COSMETIC),
        ("p54a", REMOVED),
        ("p99", ADDED),
    ]
    removed = changes[2]
    assert (removed.description_a, removed.description_b) == ("x", "")
    added = changes[3]
    assert (added.description_a, added.description_b) == ("", "y")
