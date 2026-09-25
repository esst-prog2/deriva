import pytest

from deriva.rule import COSMETIC, REAL, UNCHANGED, classify, normalise


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("Area", "Area", UNCHANGED),
        ("Area", "Área", COSMETIC),
        ("Rama de actividad", "rama de Actividad", COSMETIC),
        ("Ingreso  total.", "Ingreso total", COSMETIC),
        (" Ingreso total", "Ingreso total ", COSMETIC),
        ("Rama de actividad CIIU4", "Rama de actividad CIIU 4.1", REAL),
        ("Horas en el trabajo secundario", "Horas en el", REAL),
    ],
)
def test_classify(a, b, expected):
    assert classify(a, b) == expected


def test_punctuation_becomes_a_space():
    assert normalise("CIIU 4.1") == "ciiu 4 1"
    assert normalise("CIIU4") == "ciiu4"


def test_symbols_are_kept():
    assert classify("Ingreso en $", "Ingreso en %") == REAL


def test_ene_loses_its_tilde():
    # A known cost of stripping accents: "año" and "ano" normalise alike.
    assert normalise("Año") == "ano"
