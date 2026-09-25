from pathlib import Path

import pytest
from openpyxl import Workbook

DATA = Path(__file__).resolve().parent.parent / "data"
DICT_2021 = DATA / "Diccionario de Datos_persona_anual_2021.xlsx"
DICT_2025 = DATA / "Diccionario de Datos_persona_anual_2025.xlsx"

METADATA = [
    ("Institución", "Instituto Nacional de Estadistica y Censos"),
    ("Identificador", "INEC_PDA_2021"),
    ("Documento Referencia", "INEC_DIES_ENEMDU_2021"),
    ("Nombre", "BDDenemdu_personas_2021_anual"),
    ("Descripción", "La Tabla de datos de la Encuesta Nacional de Empleo"),
]
HEADER_ROW = ("Nombre del campo", "Descripción del campo")


@pytest.fixture
def make_workbook(tmp_path):
    """Write rows to a one-sheet .xlsx in tmp_path and return its path."""

    def make(rows, name="dict_2021.xlsx"):
        workbook = Workbook()
        sheet = workbook.active
        for row in rows:
            sheet.append(list(row))
        path = tmp_path / name
        workbook.save(path)
        return path

    return make
