import pytest

from deriva.rule import COSMETIC, REAL, UNCHANGED, classify
from deriva.rule_v2 import classify_v2


@pytest.mark.parametrize(
    "variable, a, b, expected",
    [
        # Everything the first rule calls cosmetic stays cosmetic.
        ("area", "Area", "Área", COSMETIC),
        ("area", "Area", "Area", UNCHANGED),
        # 1. A different reference month.
        ("p66", "En el mes de NOVIEMBRE ¿cuánto recibió?", "En el mes de MAYO ¿cuánto recibió?", COSMETIC),
        ("p69", "ganancia en el mes de septiembre", "ganancia en el mes de Diciembre", COSMETIC),
        # 2. The variable's own code repeated at the start of the text.
        ("ced01a", "CED01A. Tiene cédula de identidad", "Tiene cédula de identidad", COSMETIC),
        # 3. Abbreviated ordinals.
        ("p44j", "Recibe 13er sueldo", "Recibe 13vo sueldo", COSMETIC),
        ("p44k", "Recibe 14to sueldo", "Recibe 14vo sueldo", COSMETIC),
        # Real changes stay real.
        ("rama1", "Rama de actividad CIIU4", "Rama de actividad CIIU 4.1", REAL),
        ("p54a", "Horas en el trabajo secundario", "Horas en el", REAL),
        ("estrato", "Plan de muestreo", "Estrato", REAL),
        # A month added or removed, not swapped, is still a change.
        ("p66", "¿cuánto recibió?", "En el mes de MAYO ¿cuánto recibió?", REAL),
        # A code at the start that is not this variable's own code is kept.
        ("ced01a", "P03. Tiene cédula", "Tiene cédula", REAL),
        # A different number is not an ordinal change.
        ("p44j", "Recibe 13er sueldo", "Recibe 14vo sueldo", REAL),
    ],
)
def test_classify_v2(variable, a, b, expected):
    assert classify_v2(a, b, variable) == expected


def test_first_rule_is_unchanged():
    # The demo's 12 of 22 rests on the first rule; v2 must not change it.
    assert classify("Recibe 13er sueldo", "Recibe 13vo sueldo") == REAL
    assert classify("En el mes de NOVIEMBRE", "En el mes de MAYO") == REAL
