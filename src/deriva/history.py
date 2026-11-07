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
    BREAK: "Dictionary layout redesigned — not compared",
    SAME: "",
}

PAGE = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>deriva: how the ENEMDU questionnaire changed</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<style>
:root {{ --paper:#fcfdfe; --ink:#1c2b4a; --soft:#5a6782; --rule:#d5dfec; --grid:#eef3f9;
  --pencil:#c8102e; --graphite:#9aa3b2; --marker:#fff1a8; --new:#2f6fb5; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:15px/1.5 "Public Sans",system-ui,sans-serif; }}
.page {{ max-width:68rem; margin:0 auto; padding:2.5rem 1.5rem 4rem; }}
.mast {{ display:flex; justify-content:space-between; align-items:baseline; border-bottom:2px solid var(--ink); padding-bottom:.6rem; }}
.mast strong {{ font-weight:800; font-size:1.05rem; }}
.mast span {{ color:var(--soft); font-size:.85rem; }}
.lede {{ font:400 2.1rem/1.2 "Source Serif 4",Georgia,serif; max-width:40rem; margin:2rem 0 .8rem; letter-spacing:-.01em; }}
.lede em {{ font-style:normal; background:linear-gradient(transparent 62%,var(--marker) 62%); }}
.sub {{ color:var(--soft); max-width:40rem; margin:0 0 2rem; }}
.controls {{ display:flex; flex-wrap:wrap; gap:.8rem 1.4rem; align-items:center; padding:.9rem 0; border-top:1px solid var(--rule);
  border-bottom:1px solid var(--rule); position:sticky; top:0; background:var(--paper); z-index:3; }}
.controls input[type=search] {{ font:inherit; border:0; border-bottom:2px solid var(--ink); background:transparent; padding:.3rem 0; width:16rem; outline:none; color:var(--ink); }}
.controls input[type=search]:focus {{ border-color:var(--pencil); }}
.controls label {{ display:flex; gap:.4rem; align-items:center; color:var(--soft); font-size:.9rem; cursor:pointer; }}
.controls input[type=radio] {{ accent-color:var(--ink); }}
.shown {{ margin-left:auto; color:var(--soft); font-size:.85rem; }}
.map {{ width:100%; border-collapse:collapse; margin-top:1rem; }}
.map th {{ font-weight:600; font-size:.78rem; color:var(--soft); text-align:center; padding:.4rem 0; }}
.map th.q {{ text-align:left; }}
.map th.redesign {{ color:var(--graphite); font-weight:400; font-style:italic; }}
.map td {{ border-top:1px solid var(--grid); padding:0; }}
.map td.cell {{ width:4.2rem; text-align:center; height:2.6rem; }}
.map td.cut {{ width:1.6rem; background:repeating-linear-gradient(135deg,transparent 0 5px,var(--grid) 5px 7px); }}
.dot {{ display:inline-block; width:.8rem; height:.8rem; border-radius:50%; vertical-align:middle; }}
.dot.real {{ background:var(--pencil); }} .dot.cosmetic {{ border:2px solid var(--graphite); }}
.dot.added, .dot.removed {{ width:.9rem; height:2px; border-radius:0; background:var(--new); }}
.dot.same {{ width:4px; height:4px; background:var(--rule); }}
.dot.missing {{ width:0; }}
tr.row {{ cursor:pointer; }} tr.row:hover td {{ background:var(--grid); }}
tr.row:focus-visible {{ outline:2px solid var(--pencil); outline-offset:-2px; }}
td.q {{ padding:.45rem .8rem .45rem 0; }}
td.q b {{ font-weight:600; margin-right:.5rem; }}
td.q span {{ color:var(--soft); font-size:.86rem; }}
tr.detail td {{ border-top:0; padding:0 0 1.4rem; }}
.sheet {{ border-left:3px solid var(--ink); margin-left:.2rem; padding:.2rem 0 .2rem 1.2rem; }}
.entry {{ display:grid; grid-template-columns:5.5rem 1fr; gap:1rem; padding:.45rem 0; }}
.entry .when {{ color:var(--soft); font-size:.85rem; padding-top:.15rem; }}
.entry .text {{ font:400 1.02rem/1.6 "Source Serif 4",Georgia,serif; max-width:46rem; }}
.entry.real .when {{ color:var(--pencil); font-weight:600; }}
.entry.real .text {{ border-left:2px solid var(--pencil); margin-left:-1.32rem; padding-left:1.2rem; }}
.entry .note {{ display:block; font:600 .78rem "Public Sans",sans-serif; color:var(--pencil); margin-top:.15rem; }}
.entry.cosmetic .note {{ color:var(--graphite); }}
.entry.missing .text {{ color:var(--graphite); font-style:italic; }}
.cutline {{ color:var(--graphite); font-size:.82rem; font-style:italic; padding:.5rem 0; border-top:1px dashed var(--rule); border-bottom:1px dashed var(--rule); margin:.3rem 0; }}
del {{ color:var(--pencil); text-decoration:line-through 2px var(--pencil); }}
ins {{ text-decoration:none; background:var(--marker); }}
.key {{ display:flex; flex-wrap:wrap; gap:1.4rem; color:var(--soft); font-size:.85rem; margin:1.6rem 0 0; }}
.key span {{ display:flex; gap:.45rem; align-items:center; }}
footer {{ color:var(--soft); font-size:.82rem; margin-top:2.5rem; max-width:44rem; }}
@media (max-width:760px) {{ .lede {{ font-size:1.6rem; }} .map td.cell {{ width:2rem; }} .map th {{ font-size:.65rem; }} .shown {{ margin-left:0; }} }}
</style></head><body><div class="page">
<div class="mast"><strong>deriva</strong><span>ENEMDU persona dictionaries, INEC</span></div>
<p class="lede">Between {first} and {last}, <em>{real} questions changed</em> in a way a researcher should check.</p>
<p class="sub">{n_rounds} rounds of the survey, {variables} variables, {cosmetic} further changes that only touch the wording.
Click a question to read every version of it.</p>
<div class="controls">
<input type="search" id="q" placeholder="Find a variable, e.g. p76" aria-label="Find a variable">
<label><input type="radio" name="f" value="real" checked> Questions to check</label>
<label><input type="radio" name="f" value="changed"> Any change</label>
<label><input type="radio" name="f" value="all"> Every variable</label>
<span class="shown" id="shown"></span>
</div>
<table class="map">
<thead><tr><th class="q">Question</th>{head}</tr></thead>
<tbody>
{rows}
</tbody></table>
<div class="key"><span><i class="dot real"></i>Real change</span><span><i class="dot cosmetic"></i>Wording only</span>
<span><i class="dot added"></i>Added or removed</span><span><i class="dot same"></i>Same as before</span>
<span>Shaded column: the dictionary layout redesigned in 2021, not compared</span></div>
<footer>Each change between two consecutive rounds of the same layout is classified by deriva's second rule
(deriva-eval --rule v2), which agreed with my hand labels on 40 of 45 changes in a pair of rounds it was not built from.
In each question, struck words were removed and highlighted words were added.</footer>
</div>
<script>
const q=document.getElementById("q"), shown=document.getElementById("shown");
function filter(){{
  const t=q.value.trim().toLowerCase(), f=document.querySelector("input[name=f]:checked").value; let n=0;
  for(const r of document.querySelectorAll("tr.row")){{
    const ok=r.dataset.name.toLowerCase().includes(t) && (t || f==="all" || (f==="real" ? r.dataset.real!=="0" : r.dataset.changed!=="0"));
    r.hidden=!ok; const d=r.nextElementSibling; if(!ok) d.hidden=true; if(ok) n++;
  }}
  shown.textContent=n+(n===1?" question":" questions");
}}
function toggle(r){{ const d=r.nextElementSibling; d.hidden=!d.hidden; r.setAttribute("aria-expanded", String(!d.hidden)); }}
for(const r of document.querySelectorAll("tr.row")){{
  r.addEventListener("click",()=>toggle(r));
  r.addEventListener("keydown",e=>{{ if(e.key==="Enter"||e.key===" "){{ e.preventDefault(); toggle(r); }} }});
}}
q.addEventListener("input",()=>{{ filter(); const v=[...document.querySelectorAll("tr.row")].filter(r=>!r.hidden);
  if(v.length===1){{ v[0].nextElementSibling.hidden=false; }} }});
for(const i of document.querySelectorAll("input[name=f]")) i.addEventListener("change",filter);
filter();
</script>
</body></html>
"""

NOTE = {REAL: "Real change", COSMETIC: "Wording only", ADDED: "Added", REMOVED: "Removed"}


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


def _short(text: str, width: int = 70) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 1].rsplit(" ", 1)[0] + "…"


def render(rounds: list[Round], history: dict[str, list[Entry]]) -> str:
    head = []
    for i, r in enumerate(rounds):
        if i and rounds[i - 1].dictionary.layout != r.dictionary.layout:
            head.append('<th class="redesign" title="Dictionary layout redesigned, not compared"></th>')
        head.append(f"<th>{r.label}</th>")
    rows, real_total, cos_total = [], 0, 0
    for name, entries in history.items():
        real = sum(e.mark == REAL for e in entries)
        cosmetic = sum(e.mark == COSMETIC for e in entries)
        changed = sum(e.mark in (REAL, COSMETIC, ADDED, REMOVED) for e in entries)
        real_total += real
        cos_total += cosmetic
        latest = next((e.text for e in reversed(entries) if e.text), "")
        cells, sheet, before = [], [], None
        for e in entries:
            if e.mark == BREAK:
                cells.append('<td class="cut"></td>')
                sheet.append('<div class="cutline">Dictionary layout redesigned in 2021, not compared</div>')
            dot = "missing" if e.text is None else (e.mark if e.mark in NOTE else "same")
            cells.append(f'<td class="cell"><i class="dot {dot}" title="{e.round}"></i></td>')
            if e.text is None:
                text, kind = "Not in this round", "missing"
            elif e.mark in (REAL, COSMETIC) and before is not None:
                text, kind = _diff(before, e.text), e.mark
            else:
                text, kind = html.escape(e.text), e.mark
            note = f'<span class="note">{NOTE[e.mark]}</span>' if e.mark in NOTE else ""
            sheet.append(f'<div class="entry {kind}"><div class="when">{e.round}{note}</div><div class="text">{text}</div></div>')
            before = e.text
        n_cols = len(cells) + 1
        rows.append(
            f'<tr class="row" tabindex="0" aria-expanded="false" data-name="{html.escape(name)}" data-real="{real}" data-changed="{changed}">'
            f'<td class="q"><b>{html.escape(name)}</b><span>{html.escape(_short(latest))}</span></td>{"".join(cells)}</tr>'
            f'<tr class="detail" hidden><td colspan="{n_cols}"><div class="sheet">{"".join(sheet)}</div></td></tr>'
        )
    return PAGE.format(
        first=_month(rounds[0].label), last=rounds[-1].label,
        real=real_total, cosmetic=cos_total, n_rounds=len(rounds), variables=len(history),
        head="".join(head), rows="\n".join(rows),
    )


MONTHS = "January February March April May June July August September October November December".split()


def _month(label: str) -> str:
    year, _, month = label.partition("-")
    return f"{MONTHS[int(month) - 1]} {year}" if month else year


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
