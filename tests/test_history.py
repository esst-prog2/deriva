from pathlib import Path

import pytest

from deriva.history import BREAK, build_history, main, read_rounds, round_of
from deriva.rule import COSMETIC, REAL

from conftest import DATA, HEADER_ROW

OLD_HEADER_ROW = (None, None, "CODIGO DE LA VARIABLE", "NOMBRE DE LA VARIABLE", "PREGUNTA")


def old_rows(variables):
    return [OLD_HEADER_ROW] + [(None, None, name, name, text) for name, text in variables]


@pytest.fixture
def folder(tmp_path, monkeypatch, make_workbook):
    """Two older-layout rounds and two 2021+ rounds, with invented descriptions."""
    monkeypatch.chdir(tmp_path)
    make_workbook(old_rows([("p66", "En el mes de MAYO ¿cuánto recibió?"), ("p76", "BONO DE DESARROLLO HUMANO")]),
                  name="dict_2020_09.xlsx")
    make_workbook(old_rows([("p66", "En el mes de NOVIEMBRE ¿cuánto recibió?"), ("p76", "BONO o PENSIÓN")]),
                  name="dict_2020_12.xlsx")
    make_workbook([HEADER_ROW, ("p66", "Ingreso"), ("p76", "Bono")], name="dict_anual_2021.xlsx")
    make_workbook([HEADER_ROW, ("p66", "Ingreso"), ("p99", "Nueva")], name="dict_anual_2022.xlsx")
    return tmp_path


def test_round_of():
    assert round_of(Path("enemdu_personas_2019_06.xlsx")) == ("2019-06", (2019, 6))
    assert round_of(Path("Diccionario de Datos_persona_anual_2021.xlsx")) == ("2021", (2021, 0))


def test_history_marks(folder):
    rounds = read_rounds(folder)
    assert [r.label for r in rounds] == ["2020-09", "2020-12", "2021", "2022"]
    history = build_history(rounds)
    assert [e.mark for e in history["p66"]] == ["same", COSMETIC, BREAK, "same"]
    assert [e.mark for e in history["p76"]] == ["same", REAL, BREAK, "removed"]
    assert [e.mark for e in history["p99"]] == ["same", "same", BREAK, "added"]


def test_page_is_written(folder, capsys):
    assert main([str(folder)]) == 0
    page = (folder / "deriva_history.html").read_text(encoding="utf-8")
    assert 'data-name="p76" data-real="1"' in page
    assert "Questionnaire redesign" in page
    assert "PENSIÓN" in page
    assert "wrote" in capsys.readouterr().out


def test_empty_folder(tmp_path, capsys):
    assert main([str(tmp_path)]) == 1
    assert capsys.readouterr().err.startswith("deriva-history: error: ")


def test_p76_on_the_real_files():
    history = build_history(read_rounds(DATA))
    marks = {e.round: e.mark for e in history["p76"]}
    assert marks["2020-12"] == REAL
    assert marks["2021"] == BREAK
