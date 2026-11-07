"""The `deriva-history` command: each variable's description in every round, on one page."""

import argparse
import difflib
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
    REAL: "Real change",
    COSMETIC: "Cosmetic",
    ADDED: "Added",
    REMOVED: "Removed",
    BREAK: "Questionnaire redesign — not compared",
    SAME: "",
}

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>deriva · ENEMDU history</title>
<style>
:root {{
  --bg: #f6f7f9; --card: #fff; --ink: #1b1f24; --muted: #5d6673; --line: #e3e6ea;
  --accent: #23476b; --real: #b42318; --real-bg: #fdecea; --cos: #6b7280; --cos-bg: #f1f2f4;
  --new: #1d5fa7; --new-bg: #e8f0fb; --ins: #d6f0dd; --del: #f9d7d3;
}}
@media (prefers-color-scheme: dark) {{ :root {{
  --bg: #111418; --card: #1a1e24; --ink: #e8eaed; --muted: #9aa3ad; --line: #2a3038;
  --accent: #8fb6e0; --real: #ff8a80; --real-bg: #3a1f1d; --cos: #a0a7b0; --cos-bg: #252a31;
  --new: #8ab4f8; --new-bg: #1d2a3d; --ins: #1f3b28; --del: #4a2422;
}} }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif; }}
header {{ background: var(--accent); color: #fff; padding: 2rem 1rem 4.5rem; }}
@media (prefers-color-scheme: dark) {{ header {{ background: #1c2b3d; }} }}
.wrap {{ max-width: 72rem; margin: 0 auto; padding: 0 1rem; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; opacity: .75; margin: 0; }}
h1 {{ font-size: 1.9rem; margin: .2rem 0 .3rem; font-weight: 650; }}
.rounds {{ margin: 0; opacity: .85; font-size: .9rem; }}
.stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .8rem; margin-top: -3rem; }}
.stat {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: .9rem 1rem;
  box-shadow: 0 1px 2px rgba(0,0,0,.05); }}
.stat b {{ display: block; font-size: 1.6rem; font-weight: 650; }}
.stat span {{ color: var(--muted); font-size: .85rem; }}
.stat.real b {{ color: var(--real); }}
.toolbar {{ position: sticky; top: 0; z-index: 2; background: var(--bg); padding: 1rem 0 .8rem;
  display: flex; flex-wrap: wrap; gap: .8rem 1.2rem; align-items: center; border-bottom: 1px solid var(--line); }}
input[type=search] {{ font: inherit; padding: .55rem .8rem; width: min(22rem, 100%); border: 1px solid var(--line);
  border-radius: 8px; background: var(--card); color: var(--ink); }}
.toolbar label {{ color: var(--muted); font-size: .9rem; display: flex; gap: .4rem; align-items: center; }}
.legend {{ margin-left: auto; display: flex; gap: .5rem; flex-wrap: wrap; }}
.pill {{ display: inline-block; font-size: .72rem; font-weight: 600; letter-spacing: .02em; padding: .12rem .55rem;
  border-radius: 999px; white-space: nowrap; }}
.pill.real {{ color: var(--real); background: var(--real-bg); }}
.pill.cosmetic {{ color: var(--cos); background: var(--cos-bg); }}
.pill.added, .pill.removed {{ color: var(--new); background: var(--new-bg); }}
.count {{ color: var(--muted); font-size: .85rem; margin: .8rem 0 0; }}
section {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; margin: 1rem 0;
  padding: 1rem 1.2rem; box-shadow: 0 1px 2px rgba(0,0,0,.04); }}
section h2 {{ margin: 0 0 .6rem; font: 650 1.05rem ui-monospace, SFMono-Regular, Menlo, monospace;
  display: flex; gap: .6rem; align-items: center; }}
ol {{ list-style: none; margin: 0; padding: 0 0 0 1.2rem; border-left: 2px solid var(--line); }}
li {{ position: relative; display: grid; grid-template-columns: 5.2rem 8.5rem 1fr; gap: .8rem;
  padding: .45rem 0 .45rem .6rem; }}
li::before {{ content: ""; position: absolute; left: -1.62rem; top: .85rem; width: .7rem; height: .7rem;
  border-radius: 50%; background: var(--card); border: 2px solid var(--line); }}
li.real::before {{ background: var(--real); border-color: var(--real); }}
li.cosmetic::before {{ background: var(--cos); border-color: var(--cos); }}
li.added::before, li.removed::before {{ background: var(--new); border-color: var(--new); }}
li.real {{ background: var(--real-bg); border-radius: 8px; }}
.round {{ font: 600 .85rem ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--muted); padding-top: .1rem; }}
.missing {{ color: var(--muted); font-style: italic; }}
li.break {{ display: block; color: var(--muted); font-size: .82rem; font-style: italic; padding: .5rem .6rem;
  border-top: 1px dashed var(--muted); border-bottom: 1px dashed var(--muted); margin: .3rem 0; }}
li.break::before {{ display: none; }}
ins {{ background: var(--ins); text-decoration: none; border-radius: 3px; padding: 0 .1rem; }}
del {{ background: var(--del); border-radius: 3px; padding: 0 .1rem; }}
footer {{ color: var(--muted); font-size: .8rem; padding: 2rem 0 3rem; }}
@media (max-width: 640px) {{ .stats {{ grid-template-columns: repeat(2, 1fr); }}
  li {{ grid-template-columns: 1fr; gap: .1rem; }} .legend {{ margin-left: 0; }} }}
</style></head><body>
<header><div class="wrap">
<p class="eyebrow">deriva · ENEMDU persona dictionaries · INEC</p>
<h1>How the questionnaire changed, variable by variable</h1>
<p class="rounds">{rounds}</p>
</div></header>
<main class="wrap">
<div class="stats">
<div class="stat"><b>{n_rounds}</b><span>rounds</span></div>
<div class="stat"><b>{variables}</b><span>variables</span></div>
<div class="stat real"><b>{real}</b><span>real changes</span></div>
<div class="stat"><b>{cosmetic}</b><span>cosmetic changes</span></div>
</div>
<div class="toolbar">
<input type="search" id="q" placeholder="Search a variable, e.g. p76" autofocus>
<label><input type="checkbox" id="onlyreal"> only real changes</label>
<label><input type="checkbox" id="unchanged"> show unchanged variables</label>
<div class="legend"><span class="pill real">Real change</span><span class="pill cosmetic">Cosmetic</span><span class="pill added">Added / removed</span></div>
</div>
<p class="count" id="count"></p>
{sections}
<footer>Changes between consecutive rounds of the same layout are classified by deriva's second rule
(<code>deriva-eval --rule v2</code>); words removed are <del>struck</del>, words added are <ins>highlighted</ins>.
The 2021 redesign changed the dictionary layout, so 2020-12 and 2021 are not compared.</footer>
</main>
<script>
const q = document.getElementById("q"), only = document.getElementById("onlyreal"),
      all = document.getElementById("unchanged"), count = document.getElementById("count");
function filter() {{
  const text = q.value.trim().toLowerCase(); let shown = 0;
  for (const s of document.querySelectorAll("section")) {{
    const hit = s.dataset.name.toLowerCase().includes(text);
    const hide = !hit || (only.checked && s.dataset.real === "0") || (!all.checked && !text && s.dataset.changed === "0");
    s.hidden = hide; if (!hide) shown++;
  }}
  count.textContent = shown + " variable" + (shown === 1 ? "" : "s") + " shown";
}}
for (const el of [q, only, all]) el.addEventListener("input", filter);
filter();
</script>
</body></html>
"""


def _diff(before: str, after: str) -> str:
    """The new text, with removed words struck and added words highlighted."""
    a, b = before.split(), after.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op in ("delete", "replace"):
            out.append(f"<del>{html.escape(' '.join(a[i1:i2]))}</del>")
        if op in ("insert", "replace"):
            out.append(f"<ins>{html.escape(' '.join(b[j1:j2]))}</ins>")
        if op == "equal":
            out.append(html.escape(" ".join(a[i1:i2])))
    return " ".join(out)


def render(rounds: list[Round], history: dict[str, list[Entry]]) -> str:
    sections = []
    totals = {REAL: 0, COSMETIC: 0}
    for name, entries in history.items():
        real = sum(e.mark == REAL for e in entries)
        changed = sum(e.mark in (REAL, COSMETIC, ADDED, REMOVED) for e in entries)
        for mark in totals:
            totals[mark] += sum(e.mark == mark for e in entries)
        items, before = [], None
        for e in entries:
            if e.mark == BREAK:
                items.append(f'<li class="break">{MARK_TEXT[BREAK]}</li>')
            if e.text is None:
                text = '<span class="missing">not in this round</span>'
            elif e.mark in (REAL, COSMETIC) and before is not None:
                text = _diff(before, e.text)
            else:
                text = html.escape(e.text)
            pill = f'<span class="pill {e.mark}">{MARK_TEXT[e.mark]}</span>' if MARK_TEXT[e.mark] and e.mark != BREAK else ""
            items.append(f'<li class="{e.mark}"><span class="round">{e.round}</span><span>{pill}</span><span>{text}</span></li>')
            before = e.text
        badge = f'<span class="pill real">{real} real</span>' if real else ""
        sections.append(
            f'<section data-name="{html.escape(name)}" data-real="{real}" data-changed="{changed}">'
            f"<h2>{html.escape(name)}{badge}</h2><ol>{''.join(items)}</ol></section>"
        )
    return PAGE.format(
        rounds=" → ".join(r.label for r in rounds),
        n_rounds=len(rounds),
        variables=len(history),
        real=totals[REAL],
        cosmetic=totals[COSMETIC],
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
