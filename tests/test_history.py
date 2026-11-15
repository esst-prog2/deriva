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
    assert "Redesign break: the dictionary layout changed in 2021" in page
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


def test_hand_label_replaces_the_second_rule(folder):
    rounds = read_rounds(folder)
    hand = {("BONO DE DESARROLLO HUMANO", "BONO o PENSIÓN"): COSMETIC}
    entry = build_history(rounds, hand)["p76"][1]
    assert (entry.mark, entry.by_hand) == (COSMETIC, True)
    other = build_history(rounds, hand)["p66"][1]
    assert (other.mark, other.by_hand) == (COSMETIC, False)


def test_page_says_who_decided(folder, capsys):
    labels = folder / "labels"
    labels.mkdir()
    (labels / "labels_x.csv").write_text(
        "variable,description_a,description_b,label,note\n"
        "p76,BONO DE DESARROLLO HUMANO,BONO o PENSIÓN,real,\n",
        encoding="utf-8",
    )
    assert main([str(folder), "--labels", str(labels)]) == 0
    page = (folder / "deriva_history.html").read_text(encoding="utf-8")
    assert "Who decided each mark: double-ringed marks (1) are my hand labels; every other mark is deriva's second rule, not checked by hand." in page
    assert "dot real hand" in page


def test_p10a_on_the_real_files_shows_my_label():
    # The second rule calls this typo fix real; my hand label says cosmetic.
    from deriva.history import read_hand_labels

    history = build_history(read_rounds(DATA), read_hand_labels(DATA.parent / "eval"))
    entry = {e.round: e for e in history["p10a"]}["2020-12"]
    assert (entry.mark, entry.by_hand) == (COSMETIC, True)


def test_page_opens_already_searched_from_the_link(folder):
    # The promo page links to history.html?q=p76: the page must read ?q= and search for it.
    assert main([str(folder)]) == 0
    page = (folder / "deriva_history.html").read_text(encoding="utf-8")
    assert 'new URLSearchParams(location.search).get("q")' in page
    assert "q.value=asked; search();" in page


def test_legend_comes_before_the_table(folder):
    # A stranger must see what the marks mean before reading them.
    assert main([str(folder)]) == 0
    page = (folder / "deriva_history.html").read_text(encoding="utf-8")
    assert page.index('class="key"') < page.index('<table class="map"')
    for meaning in ("Real change", "Cosmetic change", "Added / removed", "Empty: not in this round",
                    "Redesign break: not compared", "Double ring: checked by hand"):
        assert meaning in page


def test_one_vocabulary(folder):
    # The same words as the promo page: cosmetic change, checked by hand, second rule not checked by hand.
    assert main([str(folder)]) == 0
    page = (folder / "deriva_history.html").read_text(encoding="utf-8")
    for old in ("Wording only", "my label)", "Questions to check", "Every variable"):
        assert old not in page
    assert "Cosmetic change (second rule, not checked by hand)" in page
    assert "Real changes <span class=\"n\">(1)</span>" in page
    assert "All variables <span class=\"n\">(3)</span>" in page


def test_phone_summary_lists_where_each_variable_changed(folder):
    # On phones the round grid is hidden; each row says where it changed instead.
    assert main([str(folder)]) == 0
    page = (folder / "deriva_history.html").read_text(encoding="utf-8")
    p76 = page[page.index('data-name="p76"'):]
    p76 = p76[: p76.index("</tr>")]
    assert '<span class="sum"><span><i class="dot real"></i>2020-12</span><span><i class="dot removed"></i>2022</span></span>' in p76
    assert ".map td.cell, .map td.cut {{ display:none; }}".replace("{{", "{").replace("}}", "}") in page
