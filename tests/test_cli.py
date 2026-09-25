import csv
import re
import shutil

import pytest

from deriva.cli import main
from deriva.output import ENCODING

from conftest import DICT_2021, DICT_2025, HEADER_ROW, METADATA


@pytest.fixture(autouse=True)
def in_tmp_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def counts(stdout):
    return {name: int(n) for name, n in re.findall(r"^\s+(\w+)\s+(\d+)$", stdout, re.M)}


def test_real_files(capsys, tmp_path):
    assert main([str(DICT_2021), str(DICT_2025)]) == 0
    out = capsys.readouterr().out
    assert "2021: 151 variables" in out
    assert "2025: 139 variables" in out
    found = counts(out)
    assert found["removed"] == 12
    assert found["added"] == 0
    # Only the total: the cosmetic/real split is what the hand labels will measure.
    assert found["cosmetic"] + found["real"] == 22
    assert (tmp_path / "deriva_2021_vs_2025.csv").is_file()


def test_same_file_twice(capsys, tmp_path):
    assert main([str(DICT_2021), str(DICT_2021)]) == 0
    found = counts(capsys.readouterr().out)
    assert [found[k] for k in ("added", "removed", "cosmetic", "real")] == [0, 0, 0, 0]
    with (tmp_path / "deriva_2021_a_vs_2021_b.csv").open(encoding=ENCODING) as f:
        assert len(list(csv.reader(f))) == 1


def test_one_argument(capsys):
    with pytest.raises(SystemExit) as exit:
        main([str(DICT_2021)])
    assert exit.value.code != 0
    assert "usage: deriva" in capsys.readouterr().err


def test_three_arguments(capsys):
    with pytest.raises(SystemExit) as exit:
        main([str(DICT_2021), str(DICT_2025), str(DICT_2025)])
    assert exit.value.code != 0
    assert "usage: deriva" in capsys.readouterr().err


def test_sheet_without_header(capsys, make_workbook):
    bad = make_workbook(METADATA + [("area", "Area")], name="bad_2025.xlsx")
    assert main([str(DICT_2021), str(bad)]) == 1
    err = capsys.readouterr().err
    assert "Nombre del campo" in err
    assert "bad_2025.xlsx" in err


def test_missing_file(capsys):
    assert main([str(DICT_2021), "nope_2025.xlsx"]) == 1
    assert "nope_2025.xlsx" in capsys.readouterr().err


def test_console_script_runs(tmp_path):
    import subprocess

    deriva = shutil.which("deriva")
    if deriva is None:
        pytest.skip("deriva console script not on PATH")
    result = subprocess.run([deriva, str(DICT_2021), str(DICT_2021)], capture_output=True, text=True)
    assert result.returncode == 0
    assert "2021_a: 151 variables" in result.stdout
