from pathlib import Path

import pytest

from deriva import DerivaError
from deriva.reader import distinct_labels, read_dictionary, round_label

from conftest import DICT_2021, DICT_2025, HEADER_ROW, METADATA

VARIABLES = [("area", "Area"), ("ciudad", "Ciudad")]


def test_header_below_metadata_rows(make_workbook):
    path = make_workbook(METADATA + [HEADER_ROW] + VARIABLES)
    assert read_dictionary(path).variables == {"area": "Area", "ciudad": "Ciudad"}


def test_header_at_a_different_row(make_workbook):
    path = make_workbook(METADATA[:1] + [HEADER_ROW] + VARIABLES)
    assert read_dictionary(path).variables == {"area": "Area", "ciudad": "Ciudad"}


def test_header_missing(make_workbook):
    path = make_workbook(METADATA + VARIABLES)
    with pytest.raises(DerivaError) as error:
        read_dictionary(path)
    assert str(path) in str(error.value)
    assert "Nombre del campo" in str(error.value)


def test_near_miss_is_not_the_header(make_workbook):
    path = make_workbook(METADATA + [("Nombre del campo:", "x")] + VARIABLES)
    with pytest.raises(DerivaError, match="Nombre del campo"):
        read_dictionary(path)


def test_extra_empty_columns(make_workbook):
    two = make_workbook([HEADER_ROW] + VARIABLES, name="two.xlsx")
    four = make_workbook(
        [HEADER_ROW + (None, None)] + [v + (None, None) for v in VARIABLES], name="four.xlsx"
    )
    assert read_dictionary(two).variables == read_dictionary(four).variables


def test_other_columns_are_ignored(make_workbook):
    path = make_workbook([HEADER_ROW] + [("area", "Area", "nota", 7)])
    assert read_dictionary(path).variables == {"area": "Area"}


def test_description_kept_verbatim(make_workbook):
    path = make_workbook([HEADER_ROW, ("p54a", "Horas  en el Trabajo Secundário ")])
    assert read_dictionary(path).variables == {"p54a": "Horas  en el Trabajo Secundário "}


def test_names_are_trimmed_and_empty_description_is_empty(make_workbook):
    path = make_workbook([HEADER_ROW, (" area ", None), ("ciudad", "Ciudad")])
    assert read_dictionary(path).variables == {"area": "", "ciudad": "Ciudad"}


def test_trailing_empty_rows(make_workbook):
    path = make_workbook([HEADER_ROW] + VARIABLES + [(None, None)] * 11)
    assert len(read_dictionary(path).variables) == 2


def test_empty_row_between_variables(make_workbook):
    path = make_workbook([HEADER_ROW, VARIABLES[0], (None, None), VARIABLES[1]])
    assert list(read_dictionary(path).variables) == ["area", "ciudad"]


def test_duplicate_name(make_workbook):
    path = make_workbook([HEADER_ROW, ("p54a", "x"), ("p54b", "y"), ("p54a", "z")])
    with pytest.raises(DerivaError) as error:
        read_dictionary(path)
    assert str(path) in str(error.value)
    assert "p54a" in str(error.value)


def test_missing_file(tmp_path):
    path = tmp_path / "nope_2021.xlsx"
    with pytest.raises(DerivaError, match="nope_2021.xlsx"):
        read_dictionary(path)


def test_not_an_xlsx_file(tmp_path):
    path = tmp_path / "notes_2021.xlsx"
    path.write_text("not a workbook")
    with pytest.raises(DerivaError, match="notes_2021.xlsx"):
        read_dictionary(path)


def test_round_label_from_real_file_names():
    assert round_label(DICT_2021) == "2021"
    assert round_label(DICT_2025) == "2025"


def test_round_label_uses_the_last_year():
    assert round_label(Path("enemdu_1999_revised_2021.xlsx")) == "2021"


def test_round_label_without_a_year():
    assert round_label(Path("dictionary_persona.xlsx")) == "dictionary_persona"


def test_same_label_twice():
    assert distinct_labels("2021", "2021") == ("2021_a", "2021_b")
    assert distinct_labels("2021", "2025") == ("2021", "2025")


def test_real_dictionaries_variable_counts():
    assert len(read_dictionary(DICT_2021).variables) == 151
    assert len(read_dictionary(DICT_2025).variables) == 139
