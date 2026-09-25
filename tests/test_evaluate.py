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


def test_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "nope.csv")]) == 1
    assert "nope.csv" in capsys.readouterr().err


def test_freshly_generated_template(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    deriva_main(["--labels-template", str(DICT_2021), str(DICT_2025)])
    capsys.readouterr()
    assert main(["labels_2021_vs_2025.csv"]) == 0
    out = capsys.readouterr().out
    assert "0 of 22 rows labelled" in out
    assert "nothing to measure yet" in out
