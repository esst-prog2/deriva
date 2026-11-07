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
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>deriva · ENEMDU questionnaire history</title>
<style>
:root {{ --bg:#f7f8fa; --card:#fff; --ink:#111827; --muted:#6b7280; --line:#e5e7eb; --soft:#f3f4f6;
  --brand:#0f3d5e; --real:#c0362c; --real-bg:#fdf0ef; --cos:#9ca3af; --new:#2563eb; --ins:#dcfce7; --del:#fee2e2; }}
* {{ box-sizing:border-box; }}
html {{ color-scheme: light; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,"Helvetica Neue",sans-serif; -webkit-font-smoothing:antialiased; }}
.wrap {{ max-width:76rem; margin:0 auto; padding:0 1.5rem; }}
.top {{ background:var(--card); border-bottom:1px solid var(--line); }}
.top .wrap {{ display:flex; align-items:center; justify-content:space-between; height:3.5rem; }}
.brand {{ font-weight:700; letter-spacing:-.01em; color:var(--brand); display:flex; gap:.5rem; align-items:center; }}
.brand i {{ width:.7rem; height:.7rem; border-radius:3px; background:var(--brand); display:inline-block; }}
.src {{ color:var(--muted); font-size:.8rem; }}
h1 {{ font-size:1.6rem; letter-spacing:-.02em; margin:2rem 0 .25rem; font-weight:700; }}
.lead {{ color:var(--muted); margin:0 0 1.5rem; }}
.grid {{ display:grid; gap:1rem; }}
.kpis {{ grid-template-columns:repeat(4,1fr); }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; }}
.kpi {{ padding:1rem 1.2rem; }}
.kpi span {{ color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.06em; font-weight:600; }}
.kpi b {{ display:block; font-size:1.9rem; font-weight:700; letter-spacing:-.02em; margin-top:.15rem; }}
.kpi.real b {{ color:var(--real); }}
.panel {{ padding:1.1rem 1.2rem 1.2rem; margin-top:1rem; }}
.panel h3 {{ margin:0 0 .9rem; font-size:.95rem; font-weight:650; }}
.bars {{ display:grid; grid-template-columns:repeat({n_steps},1fr); gap:.6rem; align-items:end; }}
.bar {{ text-align:center; font-size:.72rem; color:var(--muted); }}
.stack {{ height:110px; display:flex; flex-direction:column-reverse; border-radius:5px; overflow:hidden; background:var(--soft); }}
.stack i {{ display:block; }}
.stack .r {{ background:var(--real); }} .stack .c {{ background:var(--cos); }} .stack .n {{ background:var(--new); }}
.bar.brk .stack {{ background:repeating-linear-gradient(45deg,var(--soft),var(--soft) 6px,#e9ebee 6px,#e9ebee 12px); }}
.bar b {{ display:block; color:var(--ink); font-size:.8rem; margin-top:.35rem; }}
.key {{ display:flex; gap:1rem; margin-top:.9rem; color:var(--muted); font-size:.78rem; }}
.key i {{ width:.65rem; height:.65rem; border-radius:2px; display:inline-block; margin-right:.35rem; vertical-align:-1px; }}
.toolbar {{ position:sticky; top:0; z-index:5; background:var(--bg); padding:1rem 0; margin-top:.5rem;
  display:flex; gap:1rem; align-items:center; flex-wrap:wrap; border-bottom:1px solid var(--line); }}
input[type=search] {{ font:inherit; padding:.55rem .85rem; width:min(24rem,100%); border:1px solid var(--line);
  border-radius:8px; background:var(--card); outline:none; }}
input[type=search]:focus {{ border-color:var(--brand); box-shadow:0 0 0 3px rgba(15,61,94,.12); }}
.seg {{ display:inline-flex; border:1px solid var(--line); border-radius:8px; overflow:hidden; background:var(--card); }}
.seg button {{ font:inherit; font-size:.85rem; border:0; background:none; padding:.45rem .8rem; color:var(--muted); cursor:pointer; }}
.seg button.on {{ background:var(--brand); color:#fff; }}
.count {{ margin-left:auto; color:var(--muted); font-size:.85rem; }}
.var {{ margin:1rem 0; overflow:hidden; }}
.var header {{ display:flex; align-items:center; gap:.7rem; padding:.8rem 1.2rem; border-bottom:1px solid var(--line); }}
.var h2 {{ margin:0; font:700 1rem ui-monospace,SFMono-Regular,Menlo,monospace; }}
.var header .summary {{ color:var(--muted); font-size:.8rem; margin-left:auto; }}
table {{ width:100%; border-collapse:collapse; }}
td {{ padding:.55rem 1.2rem; border-bottom:1px solid var(--soft); vertical-align:top; }}
tr:last-child td {{ border-bottom:0; }}
td.r {{ width:6.5rem; white-space:nowrap; color:var(--muted); font:600 .8rem ui-monospace,SFMono-Regular,Menlo,monospace; padding-top:.7rem; }}
td.m {{ width:8.5rem; white-space:nowrap; }}
tr.real td {{ background:var(--real-bg); }} tr.real td.r {{ box-shadow:inset 3px 0 0 var(--real); }}
tr.missing td.t {{ color:var(--cos); font-style:italic; }}
tr.brk td {{ padding:.35rem 1.2rem; background:var(--soft); color:var(--muted); font-size:.75rem;
  text-transform:uppercase; letter-spacing:.06em; font-weight:600; }}
.tag {{ display:inline-block; font-size:.72rem; font-weight:650; padding:.12rem .5rem; border-radius:5px; }}
.tag.real {{ color:var(--real); background:#fbe1de; }} .tag.cosmetic {{ color:#4b5563; background:var(--soft); }}
.tag.added, .tag.removed {{ color:var(--new); background:#e0eafd; }}
ins {{ background:var(--ins); text-decoration:none; padding:0 .15rem; border-radius:3px; }}
del {{ background:var(--del); color:#7f1d1d; padding:0 .15rem; border-radius:3px; }}
footer {{ color:var(--muted); font-size:.78rem; padding:1.5rem 0 3rem; }}
@media (max-width:700px) {{ .kpis {{ grid-template-columns:repeat(2,1fr); }} td.m {{ width:auto; }} .count {{ margin-left:0; }} }}
</style></head><body>
<div class="top"><div class="wrap"><div class="brand"><i></i>deriva</div>
<div class="src">ENEMDU persona dictionaries · INEC, CC-BY</div></div></div>
<main class="wrap">
<h1>How the ENEMDU questionnaire changed</h1>
<p class="lead">{rounds_text}</p>
<div class="grid kpis">
<div class="card kpi"><span>Rounds</span><b>{n_rounds}</b></div>
<div class="card kpi"><span>Variables</span><b>{variables}</b></div>
<div class="card kpi real"><span>Real changes</span><b>{real}</b></div>
<div class="card kpi"><span>Cosmetic changes</span><b>{cosmetic}</b></div>
</div>
<div class="card panel"><h3>Changes between consecutive rounds</h3>
<div class="bars">{bars}</div>
<div class="key"><span><i style="background:var(--real)"></i>Real</span><span><i style="background:var(--cos)"></i>Cosmetic</span>
<span><i style="background:var(--new)"></i>Added or removed</span><span>Hatched: layout redesign, not compared</span></div></div>
<div class="toolbar">
<input type="search" id="q" placeholder="Search a variable, e.g. p76">
<div class="seg" id="seg"><button data-f="real" class="on">Real changes</button><button data-f="changed">Any change</button><button data-f="all">All variables</button></div>
<span class="count" id="count"></span>
</div>
{sections}
<footer>Each change between consecutive rounds of the same dictionary layout is classified by deriva's second rule
(<code>deriva-eval --rule v2</code>), which agreed with hand labels on 40 of 45 changes in a pair it was not built from.
Removed words are <del>marked</del>, added words are <ins>highlighted</ins>. Generated by <code>deriva-history</code>.</footer>
</main>
<script>
const q=document.getElementById("q"), seg=document.getElementById("seg"), count=document.getElementById("count");
let mode="real";
function filter(){{
  const t=q.value.trim().toLowerCase(); let n=0;
  for(const s of document.querySelectorAll(".var")){{
    const ok=s.dataset.name.toLowerCase().includes(t) && (t || mode==="all" || (mode==="real"? s.dataset.real!=="0" : s.dataset.changed!=="0"));
    s.hidden=!ok; if(ok) n++;
  }}
  count.textContent=n+(n===1?" variable":" variables");
}}
seg.addEventListener("click",e=>{{ if(!e.target.dataset.f) return; mode=e.target.dataset.f;
  for(const b of seg.children) b.classList.toggle("on", b===e.target); filter(); }});
q.addEventListener("input",filter); filter();
</script>
</body></html>
"""


def _diff(before: str, after: str) -> str:
    """The new text, with removed words marked and added words highlighted."""
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


def _bars(rounds: list[Round], history: dict[str, list[Entry]]) -> str:
    steps = []
    for i in range(1, len(rounds)):
        marks = [entries[i].mark for entries in history.values()]
        label = f"{rounds[i - 1].label} → {rounds[i].label}"
        if BREAK in marks:
            steps.append(f'<div class="bar brk"><div class="stack"></div><b>redesign</b>{label}</div>')
            continue
        r, c = marks.count(REAL), marks.count(COSMETIC)
        n = marks.count(ADDED) + marks.count(REMOVED)
        steps.append((r, c, n, label))
    peak = max([sum(x[:3]) for x in steps if isinstance(x, tuple)] + [1])
    out = []
    for x in steps:
        if isinstance(x, str):
            out.append(x)
            continue
        r, c, n, label = x
        seg = lambda k, cls: f'<i class="{cls}" style="height:{100 * k / peak:.1f}%" title="{k}"></i>' if k else ""
        out.append(f'<div class="bar"><div class="stack">{seg(r, "r")}{seg(c, "c")}{seg(n, "n")}</div>'
                   f"<b>{r} real</b>{label}</div>")
    return "".join(out)


def render(rounds: list[Round], history: dict[str, list[Entry]]) -> str:
    sections = []
    totals = {REAL: 0, COSMETIC: 0}
    for name, entries in history.items():
        real = sum(e.mark == REAL for e in entries)
        cosmetic = sum(e.mark == COSMETIC for e in entries)
        changed = sum(e.mark in (REAL, COSMETIC, ADDED, REMOVED) for e in entries)
        totals[REAL] += real
        totals[COSMETIC] += cosmetic
        rows, before = [], None
        for e in entries:
            if e.mark == BREAK:
                rows.append(f'<tr class="brk"><td colspan="3">{MARK_TEXT[BREAK]}</td></tr>')
            kind = "same" if e.mark == BREAK else e.mark
            if e.text is None:
                kind, text = "missing", "not in this round"
            elif e.mark in (REAL, COSMETIC) and before is not None:
                text = _diff(before, e.text)
            else:
                text = html.escape(e.text)
            tag = f'<span class="tag {e.mark}">{MARK_TEXT[e.mark]}</span>' if e.mark in (REAL, COSMETIC, ADDED, REMOVED) else ""
            rows.append(f'<tr class="{kind}"><td class="r">{e.round}</td><td class="m">{tag}</td><td class="t">{text}</td></tr>')
            before = e.text
        summary = f"{real} real · {cosmetic} cosmetic" if changed else "no changes"
        sections.append(
            f'<section class="card var" data-name="{html.escape(name)}" data-real="{real}" data-changed="{changed}">'
            f'<header><h2>{html.escape(name)}</h2><span class="summary">{summary}</span></header>'
            f"<table>{''.join(rows)}</table></section>"
        )
    return PAGE.format(
        rounds_text=f"{len(rounds)} rounds, {rounds[0].label} to {rounds[-1].label}: every variable's description in each round, and what changed.",
        n_rounds=len(rounds),
        variables=len(history),
        real=totals[REAL],
        cosmetic=totals[COSMETIC],
        n_steps=len(rounds) - 1,
        bars=_bars(rounds, history),
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
