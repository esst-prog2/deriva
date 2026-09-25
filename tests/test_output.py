import csv

from deriva.compare import align, classify_changes
from deriva.output import ENCODING, summary, write_changes
from deriva.reader import Dictionary


def read_csv(path):
    with path.open(encoding=ENCODING, newline="") as f:
        return list(csv.reader(f))


def test_changes_csv(tmp_path):
    a = Dictionary("2021", {"rama1": "Rama de actividad CIIU4", "p54a": "Horas, trabajo", "area": "Area"})
    b = Dictionary("2025", {"rama1": "Rama de actividad CIIU 4.1", "area": "Area"})
    alignment = align(a, b)
    path = write_changes(classify_changes(alignment), alignment, tmp_path)

    assert path.name == "deriva_2021_vs_2025.csv"
    assert path.read_bytes().startswith(b"\xef\xbb\xbf")  # BOM for Excel
    header, *rows = read_csv(path)
    assert header == ["variable", "change", "description_2021", "description_2025", "reason"]
    assert rows == [
        [
            "rama1",
            "real",
            "Rama de actividad CIIU4",
            "Rama de actividad CIIU 4.1",
            "descriptions still differ after normalising accents, case, punctuation and whitespace",
        ],
        ["p54a", "removed", "Horas, trabajo", "", "only in 2021"],
    ]


def test_changes_csv_replaces_existing_file(tmp_path):
    (tmp_path / "deriva_2021_vs_2025.csv").write_text("old")
    alignment = align(Dictionary("2021", {}), Dictionary("2025", {}))
    path = write_changes([], alignment, tmp_path)
    assert read_csv(path) == [["variable", "change", "description_2021", "description_2025", "reason"]]


def test_self_comparison_writes_header_only(tmp_path):
    variables = {"area": "Area", "ciudad": "Ciudad"}
    alignment = align(Dictionary("2021_a", variables), Dictionary("2021_b", variables))
    changes = classify_changes(alignment)
    path = write_changes(changes, alignment, tmp_path)
    assert len(read_csv(path)) == 1
    text = summary(alignment, changes, path)
    assert "unchanged     2" in text
    assert f"wrote {path}" in text
