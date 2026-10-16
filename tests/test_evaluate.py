import csv

import pytest

from deriva.cli import main as deriva_main
from deriva.evaluate import main
from deriva.output import ENCODING

from conftest import DICT_2021, DICT_2025

HEADER = ["variable", "description_2021", "description_2025", "label", "note"]
COSMETIC_PAIR = ("Area", "Área")  # the rule says cosmetic
REAL_PAIR = ("Rama CIIU4", "Rama CIIU 4.1")  # the rule says real


def write_labels(path, rows, delimiter=","):
    with path.open("w", encoding=ENCODING, newline="") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(HEADER)
        writer.writerows(rows)
    return path


def twenty_two_rows():
    """10 labelled rows: 8 agree with the rule, 2 disagree; 12 unlabelled."""
    labelled = (
        [(f"c{i}", *COSMETIC_PAIR, "cosmetic", "") for i in range(4)]
        + [(f"r{i}", *REAL_PAIR, "Real ", "") for i in range(4)]  # case and space ignored
        + [("p54a", *COSMETIC_PAIR, "real", "the word order matters here")]
        + [("rama1", *REAL_PAIR, "cosmetic", "")]
    )
    unlabelled = [(f"u{i}", *REAL_PAIR, "", "") for i in range(12)]
    return labelled + unlabelled


def test_partly_labelled_file(tmp_path, capsys):
    path = write_labels(tmp_path / "labels_2021_vs_2025.csv", twenty_two_rows())
    assert main([str(path)]) == 0
    out = capsys.readouterr().out
    assert "10 of 22 rows labelled" in out
    assert "agreement: 8 of 10 (80%)" in out
    assert "  you: cosmetic               4           1" in out
    assert "  you: real                   1           4" in out
    assert "disagreements: 2" in out
    # Hand-real/rule-cosmetic is listed first, with both descriptions and the note.
    first, second = out.index("p54a  you: real  rule: cosmetic"), out.index("rama1  you: cosmetic  rule: real")
    assert first < second
    assert "    2021: Area\n    2025: Área\n    note: the word order matters here" in out


def test_empty_template(tmp_path, capsys):
    rows = [(f"v{i}", *REAL_PAIR, "", "") for i in range(22)]
    path = write_labels(tmp_path / "labels.csv", rows)
    assert main([str(path)]) == 0
    out = capsys.readouterr().out
    assert "0 of 22 rows labelled" in out
    assert "nothing to measure yet" in out


def test_invalid_label(tmp_path, capsys):
    path = write_labels(tmp_path / "labels.csv", [("p54a", *REAL_PAIR, "maybe", "")])
    assert main([str(path)]) == 1
    err = capsys.readouterr().err
    assert err.startswith("deriva-eval: error: ")
    assert "p54a" in err and "maybe" in err


def test_semicolon_delimited_file(tmp_path, capsys):
    rows = [("p54a", "Horas, en el trabajo", "Horas en el", "real", "")]
    path = write_labels(tmp_path / "labels.csv", rows, delimiter=";")
    assert main([str(path)]) == 0
    assert "agreement: 1 of 1 (100%)" in capsys.readouterr().out


def test_multiline_description(tmp_path, capsys):
    path = write_labels(tmp_path / "labels.csv", [("p54a", "Horas\nen el", "Horas en el", "cosmetic", "")])
    assert main([str(path)]) == 0
    assert "agreement: 1 of 1 (100%)" in capsys.readouterr().out


def test_wrong_columns(tmp_path, capsys):
    path = tmp_path / "labels.csv"
    path.write_text("name,description\np54a,x\n", encoding=ENCODING)
    assert main([str(path)]) == 1
    assert "expected the columns" in capsys.readouterr().err


def test_columns_reordered_with_an_extra_column(tmp_path, capsys):
    path = tmp_path / "labels.csv"
    with path.open("w", encoding=ENCODING, newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "variable", "note", "description_2025", "description_2021", "extra"])
        writer.writerow(["real", "p54a", "", "Área", "Area", "ignored"])
    assert main([str(path)]) == 0
    out = capsys.readouterr().out
    assert "p54a  you: real  rule: cosmetic" in out
    assert "    2025: Área\n    2021: Area" in out


def test_empty_file(tmp_path, capsys):
    path = tmp_path / "labels.csv"
    path.write_text("", encoding=ENCODING)
    assert main([str(path)]) == 1
    err = capsys.readouterr().err
    assert "labels.csv" in err and "empty" in err


def test_identical_descriptions(tmp_path, capsys):
    path = write_labels(tmp_path / "labels.csv", [("area", "Area", "Area", "", "")])
    assert main([str(path)]) == 1
    err = capsys.readouterr().err
    assert "labels.csv" in err and "'area'" in err


def test_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "nope.csv")]) == 1
    assert "nope.csv" in capsys.readouterr().err


def test_freshly_generated_template(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert deriva_main(["--labels-template", str(DICT_2021), str(DICT_2025)]) == 0
    capsys.readouterr()
    assert main(["labels_2021_vs_2025.csv"]) == 0
    out = capsys.readouterr().out
    assert "0 of 22 rows labelled" in out
    assert "nothing to measure yet" in out


def test_windows_1252_file(tmp_path, capsys):
    path = tmp_path / "labels.csv"
    path.write_bytes(",".join(HEADER).encode("cp1252") + b"\r\narea,Area,\xc1rea,cosmetic,\r\n")
    assert main([str(path)]) == 1
    err = capsys.readouterr().err
    assert err.startswith("deriva-eval: error: ")
    assert "labels.csv" in err and '"CSV UTF-8"' in err


@pytest.mark.parametrize(
    "row, fields",
    [
        ("rama1,Rama CIIU4,Rama CIIU 4.1", 3),  # label and note cut off
        ("rama1,Rama CIIU4,Rama CIIU 4.1,real,,extra", 6),
    ],
)
def test_row_with_wrong_number_of_fields(tmp_path, capsys, row, fields):
    path = tmp_path / "labels.csv"
    path.write_text(f"{','.join(HEADER)}\narea,Area,Área,cosmetic,\n{row}\n", encoding=ENCODING)
    assert main([str(path)]) == 1
    err = capsys.readouterr().err
    assert "labels.csv" in err and f"row 3 has {fields} fields; the header has 5" in err


@pytest.mark.parametrize(
    "row",
    [
        'area,"Area,Área,cosmetic,',  # the rest of the file becomes one description
        'area,Area,Área,cosmetic,"forgot to close',  # the rest of the file becomes the note
    ],
)
def test_unclosed_quote(tmp_path, capsys, row):
    path = tmp_path / "labels.csv"
    path.write_text(
        f"{','.join(HEADER)}\n{row}\nrama1,Rama CIIU4,Rama CIIU 4.1,real,\n", encoding=ENCODING
    )
    assert main([str(path)]) == 1
    err = capsys.readouterr().err
    assert "labels.csv" in err and "row 2 cannot be read as CSV" in err


def test_row_numbers_count_a_multiline_cell_as_one_row(tmp_path, capsys):
    path = write_labels(tmp_path / "labels.csv", [("p54a", "Horas\nen el", "Horas en el", "cosmetic", "")])
    with path.open("a", encoding="utf-8", newline="") as f:
        f.write("rama1,Rama CIIU4\r\n")
    assert main([str(path)]) == 1
    assert "row 3 has 2 fields" in capsys.readouterr().err


def test_duplicate_variable(tmp_path, capsys):
    path = write_labels(tmp_path / "labels.csv", [("p54a", *COSMETIC_PAIR, "cosmetic", ""), ("p54a", *COSMETIC_PAIR, "real", "")])
    assert main([str(path)]) == 1
    err = capsys.readouterr().err
    assert "labels.csv" in err and "'p54a' appears more than once (again in row 3)" in err
