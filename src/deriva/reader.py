"""Reading one ENEMDU variable dictionary workbook as INEC publishes it."""

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree.ElementTree import ParseError

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from deriva import DerivaError

HEADER = "Nombre del campo"
# INEC's older layout (before 2021): name and question columns, anywhere in the header row.
OLD_NAME_HEADER = "CODIGO DE LA VARIABLE"
OLD_DESCRIPTION_HEADER = "PREGUNTA"
YEAR = re.compile(r"(?<!\d)(?:19|20)\d\d(?!\d)")  # not part of a longer run of digits


@dataclass
class Dictionary:
    label: str
    variables: dict[str, str]  # variable name -> description, in sheet order
    layout: str = "2021"  # "2021" for the Nombre del campo layout, "pre-2021" for the older one


def round_label(path: Path) -> str:
    """The last standalone 19xx/20xx year in the file name, or the file name without extension."""
    years = YEAR.findall(path.stem)
    return years[-1] if years else path.stem


def distinct_labels(label_a: str, label_b: str) -> tuple[str, str]:
    """Suffix the two labels with _a and _b when they would otherwise be the same."""
    if label_a == label_b:
        return f"{label_a}_a", f"{label_b}_b"
    return label_a, label_b


def read_dictionary(path: str | Path) -> Dictionary:
    """Read the variable names and descriptions below the `Nombre del campo` header,
    or below the older layout's `CODIGO DE LA VARIABLE` / `PREGUNTA` header."""
    path = Path(path)
    if not path.is_file():
        raise DerivaError(f"{path}: file not found")
    try:
        workbook = load_workbook(path, read_only=True, data_only=True)
    # openpyxl 3.1.5 raises AttributeError on any chartsheet when reading read-only.
    except (OSError, zipfile.BadZipFile, InvalidFileException, KeyError, ParseError, AttributeError) as exc:
        raise DerivaError(f"{path}: cannot be opened as an .xlsx workbook ({exc})") from exc

    try:
        rows = workbook.worksheets[0].iter_rows(values_only=True)
        variables, layout = _read_variables(path, rows)
    except ParseError as exc:  # sheet XML is parsed only while the rows are read
        raise DerivaError(f"{path}: first sheet cannot be read ({exc})") from exc
    finally:
        workbook.close()
    return Dictionary(label=round_label(path), variables=variables, layout=layout)


def _header_columns(row) -> tuple[int, int, str] | None:
    """(name column, description column, layout) if this row is a header of either layout."""
    cells = [_text(value) for value in row]
    if cells and cells[0] == HEADER:
        return 0, 1, "2021"
    if OLD_NAME_HEADER in cells and OLD_DESCRIPTION_HEADER in cells:
        return cells.index(OLD_NAME_HEADER), cells.index(OLD_DESCRIPTION_HEADER), "pre-2021"
    return None


def _read_variables(path: Path, rows) -> tuple[dict[str, str], str]:
    columns = None
    variables: dict[str, str] = {}
    for row_number, row in enumerate(rows, start=1):
        if columns is None:
            columns = _header_columns(row)
            continue
        padded = tuple(row) + (None,) * (max(columns[:2]) + 1)
        name, description = _text(padded[columns[0]]), _text(padded[columns[1]], strip=False)
        if not name and not description:
            continue
        if not name:
            raise DerivaError(f"{path}: row {row_number} has a description but no variable name")
        if name in variables:
            raise DerivaError(f"{path}: variable {name!r} appears more than once (again in row {row_number})")
        variables[name] = description

    if columns is None:
        raise DerivaError(
            f"{path}: no header row found; looked for {HEADER!r} in the first column, "
            f"or {OLD_NAME_HEADER!r} with {OLD_DESCRIPTION_HEADER!r} in one row"
        )
    if not variables:
        raise DerivaError(f"{path}: no variables found below the header")
    return variables, columns[2]


def _text(value, strip: bool = True) -> str:
    if value is None:
        return ""
    text = str(value)
    return text.strip() if strip else text
