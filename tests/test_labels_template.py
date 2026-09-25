import csv
import re

import pytest

from deriva.cli import main
from deriva.output import ENCODING

from conftest import DICT_2021, DICT_2025

VERDICT = re.compile(r"\b(cosmetic|real)\b", re.IGNORECASE)
TEMPLATE = "labels_2021_vs_2025.csv"


@pytest.fixture(autouse=True)
def in_tmp_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def run_template():
    return main(["--labels-template", str(DICT_2021), str(DICT_2025)])


def test_template_on_real_files(tmp_path):
    assert run_template() == 0
    with (tmp_path / TEMPLATE).open(encoding=ENCODING, newline="") as f:
        header, *rows = list(csv.reader(f))
    assert header == ["variable", "description_2021", "description_2025", "label", "note"]
    assert len(rows) == 22
    for variable, description_a, description_b, label, note in rows:
        assert variable and description_a != description_b
        assert label == "" and note == ""


def test_no_changes_csv_is_written(tmp_path):
    run_template()
    assert list(tmp_path.glob("deriva_*.csv")) == []


def test_no_verdict_leaks(tmp_path, capsys):
    run_template()
    captured = capsys.readouterr()
    written = (tmp_path / TEMPLATE).read_text(encoding=ENCODING)
    # Descriptions themselves could contain the word, so only the non-description text
    # is checked: stdout, and the header and variable/label/note columns of the file.
    assert not VERDICT.search(captured.out + captured.err)
    for row in csv.reader(written.splitlines()):
        assert not VERDICT.search(" ".join([row[0], *row[3:]]))
    assert "22 rows to label" in captured.out


def test_existing_template_is_never_overwritten(tmp_path, capsys):
    run_template()
    path = tmp_path / TEMPLATE
    path.write_bytes(path.read_bytes() + "p54a,x,y,real,labelled by hand\n".encode())
    before = path.read_bytes()

    assert run_template() == 1
    assert path.read_bytes() == before
    assert TEMPLATE in capsys.readouterr().err
