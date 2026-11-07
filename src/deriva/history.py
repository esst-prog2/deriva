"""The `deriva-history` command: each variable's description in every round, on one page."""

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from deriva import DerivaError
from deriva.reader import Dictionary, read_dictionary
from deriva.rule import COSMETIC, REAL
from deriva.rule_v2 import classify_v2

OUTPUT = "deriva_history.html"
# The last 19xx/20xx year in the file name, optionally followed by _MM for a quarterly round.
ROUND = re.compile(r"(?<!\d)((?:19|20)\d\d)(?:_(\d\d))?(?!\d)")
ADDED, REMOVED, BREAK, SAME = "added", "removed", "break", "same"


@dataclass
class Round:
    label: str  # "2019-06" for a quarterly round, "2021" for an annual one
    key: tuple[int, int]
    dictionary: Dictionary


@dataclass
class Entry:
    round: str
    text: str | None  # None when the variable is not in this round
    mark: str  # compared with the previous round: real, cosmetic, added, removed, break, same


def round_of(path: Path) -> tuple[str, tuple[int, int]]:
    matches = ROUND.findall(path.stem)
    if not matches:
        raise DerivaError(f"{path}: no year in the file name, so the round cannot be ordered")
    year, month = matches[-1]
    label = f"{year}-{month}" if month else year
    return label, (int(year), int(month or 0))


def read_rounds(folder: Path) -> list[Round]:
    paths = sorted(folder.glob("*.xlsx"))
    if not paths:
        raise DerivaError(f"{folder}: no .xlsx dictionaries found")
    rounds = []
    for path in paths:
        label, key = round_of(path)
        rounds.append(Round(label, key, read_dictionary(path)))
    rounds.sort(key=lambda r: r.key)
    labels = [r.label for r in rounds]
    repeated = [label for label in labels if labels.count(label) > 1]
    if repeated:
        raise DerivaError(f"{folder}: more than one dictionary for round {repeated[0]}")
    return rounds


def build_history(rounds: list[Round]) -> dict[str, list[Entry]]:
    """variable -> one entry per round, in order of first appearance."""
    names = list(dict.fromkeys(name for r in rounds for name in r.dictionary.variables))
    history = {}
    for name in names:
        entries, previous = [], None
        for r in rounds:
            text = r.dictionary.variables.get(name)
            if previous is None:
                mark = SAME
            elif previous.dictionary.layout != r.dictionary.layout:
                mark = BREAK
            else:
                before = previous.dictionary.variables.get(name)
                if before is None and text is None:
                    mark = SAME
                elif before is None:
                    mark = ADDED
                elif text is None:
                    mark = REMOVED
                elif before == text:
                    mark = SAME
                else:
                    mark = classify_v2(before, text, name)
            entries.append(Entry(r.label, text, mark))
            previous = r
        history[name] = entries
    return history


MARK_TEXT = {
    REAL: "real change",
    COSMETIC: "cosmetic change",
    ADDED: "added",
    REMOVED: "removed",
    BREAK: "questionnaire redesign: not compared",
    SAME: "",
}

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>deriva history</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 70rem; padding: 0 1rem; color: #222; }}
h1 {{ margin-bottom: .2rem; }} .sub {{ color: #666; margin-top: 0; }}
.controls {{ position: sticky; top: 0; background: #fff; padding: .6rem 0; border-bottom: 1px solid #ddd; }}
input[type=search] {{ font-size: 1.1rem; padding: .4rem .6rem; width: 18rem; }}
section {{ margin: 1.4rem 0; }} h2 {{ font-family: ui-monospace, monospace; margin: 0 0 .3rem; }}
table {{ border-collapse: collapse; width: 100%; }}
td {{ border-top: 1px solid #eee; padding: .35rem .5rem; vertical-align: top; }}
td.round {{ width: 6rem; font-family: ui-monospace, monospace; white-space: nowrap; }}
td.mark {{ width: 11rem; white-space: nowrap; font-size: .9rem; }}
tr.real td {{ background: #fde2e1; }} tr.real td.mark {{ color: #a1201b; font-weight: 600; }}
tr.cosmetic td.mark {{ color: #666; }} tr.added td.mark, tr.removed td.mark {{ color: #1c5fa8; }}
tr.break td {{ background: #f2f2f2; color: #555; font-style: italic; }}
td.missing {{ color: #aaa; }}
</style></head><body>
<h1>deriva history</h1>
<p class="sub">{rounds} &middot; {variables} variables &middot; {real} real changes (second rule)</p>
<div class="controls">
<input type="search" id="q" placeholder="Search a variable, e.g. p76" autofocus>
<label><input type="checkbox" id="onlyreal"> only variables with a real change</label>
</div>
{sections}
<script>
const q = document.getElementById("q"), only = document.getElementById("onlyreal");
function filter() {{
  const text = q.value.trim().toLowerCase();
  for (const s of document.querySelectorAll("section")) {{
    const hit = s.dataset.name.toLowerCase().includes(text);
    s.hidden = !hit || (only.checked && s.dataset.real === "0");
  }}
}}
q.addEventListener("input", filter); only.addEventListener("change", filter);
</script>
</body></html>
"""


def render(rounds: list[Round], history: dict[str, list[Entry]]) -> str:
    sections, real_total = [], 0
    for name, entries in history.items():
        real = sum(e.mark == REAL for e in entries)
        real_total += real
        rows = []
        for e in entries:
            if e.mark == BREAK:
                rows.append(f'<tr class="break"><td colspan="3">{MARK_TEXT[BREAK]}</td></tr>')
            text = '<td class="missing">not in this round</td>' if e.text is None else f"<td>{html.escape(e.text)}</td>"
            mark = "" if e.mark == BREAK else MARK_TEXT[e.mark]
            rows.append(f'<tr class="{e.mark}"><td class="round">{e.round}</td><td class="mark">{mark}</td>{text}</tr>')
        sections.append(
            f'<section data-name="{html.escape(name)}" data-real="{real}"><h2>{html.escape(name)}</h2>'
            f"<table>{''.join(rows)}</table></section>"
        )
    return PAGE.format(
        rounds=" &rarr; ".join(r.label for r in rounds),
        variables=len(history),
        real=real_total,
        sections="\n".join(sections),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="deriva-history",
        description="Write deriva_history.html: each variable's description in every round of a folder.",
    )
    parser.add_argument("folder", help="folder with one persona dictionary (.xlsx) per round")
    args = parser.parse_args(argv)
    try:
        rounds = read_rounds(Path(args.folder))
        history = build_history(rounds)
        path = Path.cwd() / OUTPUT
        try:
            path.write_text(render(rounds, history), encoding="utf-8")
        except OSError as exc:
            raise DerivaError(f"{path}: cannot be written ({exc.strerror})") from exc
    except DerivaError as error:
        print(f"deriva-history: error: {error}", file=sys.stderr)
        return 1
    real = sum(e.mark == REAL for entries in history.values() for e in entries)
    print(f"{len(rounds)} rounds, {len(history)} variables, {real} real changes")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
