"""Spike, 2026-11-07: are there description changes outside the 22 labelled ones?

Counts only. It prints no descriptions and no cosmetic/real verdicts, so any pair found
here stays unseen for labelling. The 2019-12 and 2020-09 dictionaries use INEC's older
layout (header 'CODIGO DE LA VARIABLE' in column C, with name and question columns),
which deriva's reader does not read, so this script reads them directly.
"""

import csv
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OLD_HEADER = "CODIGO DE LA VARIABLE"


def read_old(path):
    """variable -> (name, question) from the pre-2021 layout."""
    rows = load_workbook(path, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)
    variables, columns = {}, None
    for row in rows:
        cells = [str(c).strip() if c is not None else "" for c in row]
        if columns is None:
            if OLD_HEADER in cells:
                start = cells.index(OLD_HEADER)
                columns = (start, start + 1, start + 2)
            continue
        code, name, question = (cells + [""] * 3)[columns[0]], cells[columns[1]], cells[columns[2]]
        if code:
            variables[code] = (name, question)
    return variables


def read_new(path):
    """variable -> description from the 2021+ layout."""
    rows = load_workbook(path, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)
    variables, found = {}, False
    for row in rows:
        name, description = (list(row) + [None, None])[:2]
        if not found:
            found = str(name or "").strip() == "Nombre del campo"
            continue
        if name is not None and str(name).strip():
            variables[str(name).strip()] = str(description or "")
    return variables


def differing(a, b, pick_a, pick_b):
    shared = [k for k in a if k in b]
    return shared, {k for k in shared if pick_a(a[k]) != pick_b(b[k])}


def main():
    labelled = {
        r["variable"]
        for r in csv.DictReader((ROOT / "eval" / "labels_2021_vs_2025.csv").open(encoding="utf-8-sig"), delimiter=";")
    }
    d19 = read_old(DATA / "enemdu_personas_2019_12.xlsx")
    d20 = read_old(DATA / "diccionario_enemdu_personas_2020_09.xlsx")
    d21 = read_new(DATA / "Diccionario de Datos_persona_anual_2021.xlsx")
    print(f"variables: 2019-12 {len(d19)}, 2020-09 {len(d20)}, 2021 {len(d21)}")

    for field, i in (("name", 0), ("question", 1)):
        shared, diff = differing(d19, d20, lambda v: v[i], lambda v: v[i])
        print(f"2019-12 vs 2020-09, {field}: {len(shared)} shared, {len(diff)} differ, "
              f"{len(diff & labelled)} of them among my 22 labelled variables")

    for tag, old in (("2019-12", d19), ("2020-09", d20)):
        for field, i in (("name", 0), ("question", 1)):
            shared, diff = differing(old, d21, lambda v: v[i], lambda v: v)
            print(f"{tag} {field} vs 2021 description: {len(shared)} shared, {len(diff)} differ, "
                  f"{len(diff & labelled)} among my 22")


if __name__ == "__main__":
    main()
