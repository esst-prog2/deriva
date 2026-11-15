"""The `deriva-history` command: each variable's description in every round, on one page."""

import argparse
import difflib
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from deriva import DerivaError
from deriva.evaluate import read_labels
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
    by_hand: bool = False  # the mark is my hand label, not the second rule's verdict


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


def read_hand_labels(folder: Path) -> dict[tuple[str, str], str]:
    """(description before, description after) -> my label, from every labels_*.csv in folder."""
    labels = {}
    for path in sorted(folder.glob("labels_*.csv")):
        for row in read_labels(path).rows:
            if row.label is not None:
                labels[(row.description_a, row.description_b)] = row.label
    return labels


def build_history(rounds: list[Round], hand: dict[tuple[str, str], str] | None = None) -> dict[str, list[Entry]]:
    """variable -> one entry per round, in order of first appearance.

    A change I labelled by hand gets my label; every other change gets the second rule's."""
    hand = hand or {}
    names = list(dict.fromkeys(name for r in rounds for name in r.dictionary.variables))
    history = {}
    for name in names:
        entries, previous = [], None
        for r in rounds:
            text = r.dictionary.variables.get(name)
            by_hand = False
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
                elif (before, text) in hand:
                    mark, by_hand = hand[(before, text)], True
                else:
                    mark = classify_v2(before, text, name)
            entries.append(Entry(r.label, text, mark, by_hand))
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
.lede em {{ font-style:normal; font-weight:600; }}
.sub {{ color:var(--soft); max-width:40rem; margin:0 0 2rem; }}
.controls {{ display:flex; flex-wrap:wrap; gap:.8rem 1.4rem; align-items:center; padding:.9rem 0; border-top:1px solid var(--rule);
  border-bottom:1px solid var(--rule); position:sticky; top:0; background:var(--paper); z-index:3; }}
.controls input[type=search] {{ font:inherit; border:0; border-bottom:2px solid var(--ink); background:transparent; padding:.3rem 0; width:16rem; outline:none; color:var(--ink); }}
.controls input[type=search]:focus {{ border-color:var(--pencil); }}
.controls label {{ display:flex; gap:.4rem; align-items:center; color:var(--ink); font-size:.9rem; cursor:pointer; }}
.controls label .n {{ color:var(--soft); }}
.controls input[type=radio] {{ accent-color:var(--ink); }}
.shown {{ margin-left:auto; color:var(--soft); font-size:.85rem; }}
.map {{ width:100%; border-collapse:collapse; margin-top:1rem; }}
.map thead th {{ position:sticky; top:var(--bar,0px); background:var(--paper); z-index:2; box-shadow:0 1px 0 var(--rule); }}
.map th {{ font-weight:600; font-size:.78rem; color:var(--soft); text-align:center; padding:.4rem 0; }}
.map th.q {{ text-align:left; }}
.map th.redesign {{ color:var(--soft); font-weight:400; font-style:italic; }}
.map td {{ border-top:1px solid var(--grid); padding:0; }}
.map td.cell {{ width:4.2rem; text-align:center; height:2.6rem; }}
.map td.cut {{ width:4.2rem; background:repeating-linear-gradient(135deg,transparent 0 5px,var(--grid) 5px 7px); }}
.dot {{ display:inline-block; width:.8rem; height:.8rem; border-radius:50%; vertical-align:middle; }}
.dot.real {{ background:var(--pencil); }} .dot.cosmetic {{ border:2px solid var(--graphite); }}
.dot.added, .dot.removed {{ width:.9rem; height:2px; border-radius:0; background:var(--ink); }}
.dot.hand {{ box-shadow:0 0 0 3px var(--paper),0 0 0 4.5px var(--ink); }}
.key .dot.hand {{ margin:0 .15rem 0 .3rem; }}
.map th small {{ display:block; font-weight:400; font-size:.68rem; color:var(--ink); height:1rem; }}
.who {{ color:var(--ink); font-size:.9rem; max-width:48rem; margin:1rem 0 0; }}
.who details {{ color:var(--soft); margin-top:.3rem; }}
.who summary {{ cursor:pointer; color:var(--ink); text-decoration:underline; text-underline-offset:.2em; width:max-content; }}
.who details p {{ margin:.4rem 0 0; }}
.dot.same {{ width:4px; height:4px; background:var(--rule); }}
.dot.missing {{ width:0; }}
tr.row {{ cursor:pointer; }} tr.row:hover td {{ background:var(--grid); }}
tr.row:focus-visible {{ outline:2px solid var(--pencil); outline-offset:-2px; }}
td.q {{ padding:.45rem .8rem .45rem 0; max-width:22rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
td.q b {{ font-weight:600; margin-right:.5rem; }}
td.q span {{ color:var(--soft); font-size:.86rem; }}
tr.detail td {{ border-top:0; padding:0 0 1.4rem; }}
.sheet {{ border-left:3px solid var(--ink); margin-left:.2rem; padding:.2rem 0 .2rem 1.2rem; }}
.entry {{ display:grid; grid-template-columns:8.5rem 1fr; gap:1rem; padding:.45rem 0; }}
.entry .when {{ color:var(--soft); font-size:.85rem; padding-top:.15rem; }}
.entry .text {{ font:400 1.02rem/1.6 "Source Serif 4",Georgia,serif; max-width:46rem; }}
.entry.real .when {{ color:var(--pencil); font-weight:600; }}
.entry.real .text {{ border-left:2px solid var(--pencil); margin-left:-1.32rem; padding-left:1.2rem; }}
.entry .note {{ display:block; font:600 .78rem "Public Sans",sans-serif; color:var(--pencil); margin-top:.15rem; }}
.entry .note .by {{ display:block; font-weight:400; }}
.entry.cosmetic .note {{ color:var(--soft); }}
.entry.missing .text {{ color:var(--graphite); font-style:italic; }}
.cutline {{ color:var(--soft); font-size:.82rem; font-style:italic; padding:.5rem 0; border-top:1px dashed var(--rule); border-bottom:1px dashed var(--rule); margin:.3rem 0; }}
del {{ color:var(--soft); text-decoration:line-through 1.5px var(--soft); }}
.entry.real del {{ color:var(--pencil); text-decoration-color:var(--pencil); }}
ins {{ text-decoration:none; background:var(--marker); }}
.key {{ flex-basis:100%; display:flex; flex-wrap:wrap; gap:.4rem 1.2rem; color:var(--ink); font-size:.82rem; margin:0; padding-top:.6rem; border-top:1px solid var(--grid); }}
.key .swatch {{ display:inline-block; width:1.4rem; height:.8rem; background:repeating-linear-gradient(135deg,transparent 0 5px,var(--rule) 5px 7px); vertical-align:middle; }}
.key .blank {{ display:inline-block; width:.8rem; height:.8rem; border:1px dashed var(--soft); vertical-align:middle; }}
.key span {{ display:flex; gap:.45rem; align-items:center; }}
footer {{ color:var(--soft); font-size:.82rem; margin-top:2.5rem; max-width:44rem; }}
.sum {{ display:none; }}
/* Phones: no round grid. Each row lists where it changed; the opened wording wraps. */
@media (max-width:760px) {{
  .page {{ padding:1.5rem 1rem 3rem; }}
  .lede {{ font-size:1.6rem; }}
  .controls {{ position:static; }} .controls input[type=search] {{ width:100%; }} .shown {{ margin-left:0; }}
  .map thead th:not(.q), .map td.cell, .map td.cut {{ display:none; }}
  .map thead th {{ position:static; }}
  td.q {{ white-space:normal; max-width:none; padding:.6rem 0; }}
  td.q > span:not(.sum) {{ display:block; }}
  .sum {{ display:flex; flex-wrap:wrap; gap:.3rem .9rem; margin-top:.35rem; font-size:.82rem; color:var(--soft); }}
  td.q .sum span {{ display:inline-flex; align-items:center; gap:.4rem; }}
  .sum .dot.hand {{ margin:0 .2rem; }}
  .sheet {{ padding-left:.8rem; }}
  .entry {{ grid-template-columns:1fr; gap:.2rem; }}
  .entry .when {{ display:flex; flex-wrap:wrap; gap:.15rem .6rem; align-items:baseline; }}
  .entry .note {{ margin-top:0; }} .entry .note .by {{ display:inline; }} .entry .note .by::before {{ content:" · "; }}
  .entry.real .text {{ margin-left:-.92rem; padding-left:.8rem; }}
  .entry .text {{ overflow-wrap:break-word; }}
}}
</style></head><body><div class="page">
<div class="mast"><strong>deriva</strong><span>ENEMDU persona dictionaries, INEC</span></div>
<p class="lede">Between {first} and {last}, <em>{real} questions changed</em> in a way a researcher should check.</p>
<p class="sub">{n_rounds} rounds of the survey, {variables} variables, {cosmetic} cosmetic changes that only touch the wording.
Click a row to read every version of that question.</p>
<div class="controls">
<input type="search" id="q" placeholder="Find a variable, e.g. p76" aria-label="Find a variable">
<label><input type="radio" name="f" value="real" checked><i class="dot real"></i>Real changes <span class="n">({real})</span></label>
<label><input type="radio" name="f" value="changed"><i class="dot cosmetic"></i>Any change <span class="n">({changed_vars})</span></label>
<label><input type="radio" name="f" value="all"><i class="dot same"></i>All variables <span class="n">({variables})</span></label>
<span class="shown" id="shown"></span>
<div class="key" aria-label="What the marks mean"><span><i class="dot real"></i>Real change</span><span><i class="dot cosmetic"></i>Cosmetic change</span><span><i class="dot added"></i>Added / removed</span><span><i class="dot same"></i>Same</span><span><i class="blank"></i>Empty: nothing to compare (not in this round, or just after the redesign)</span><span><i class="swatch"></i>Redesign break: not compared</span><span><i class="dot real hand"></i>Double ring: checked by hand</span></div>
</div>
<div class="who"><p style="margin:0">Who decided each mark: double-ringed marks ({hand}) are my hand labels; every other red dot or grey ring is deriva's second rule, not checked by hand. Added, removed and same come straight from the dictionaries.</p>
<details><summary>How the marks were decided</summary>
<p>I labelled changes by hand between {hand_steps}. A label applies to every change with exactly the same wording before and after, so one label can mark several variables and rounds; that is why {hand} marks carry a hand label.</p>
<p>Every other red dot or grey ring is the verdict of deriva's second rule. No one has checked those marks one by one; tested on a pair of rounds it was not built from (September vs December 2020), the second rule agreed with my labels on 40 of 45 changes and hid none of the 7 real ones.</p>
</details></div>
<table class="map">
<thead><tr><th class="q">Question</th>{head}</tr></thead>
<tbody>
{rows}
</tbody></table>
<footer>In each question, struck words were removed and highlighted words were added.
Generated by deriva-history from the INEC dictionaries in data/ and my labels in eval/.</footer>
</div>
<script>
const q=document.getElementById("q"), shown=document.getElementById("shown");
// Column headers stick just under the sticky controls bar.
const bar=document.querySelector(".controls"), place=()=>document.documentElement.style.setProperty("--bar", bar.offsetHeight+"px");
place(); addEventListener("resize", place);
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
function search(){{ filter(); const v=[...document.querySelectorAll("tr.row")].filter(r=>!r.hidden);
  if(v.length===1){{ v[0].nextElementSibling.hidden=false; v[0].setAttribute("aria-expanded","true"); }} }}
q.addEventListener("input",search);
for(const i of document.querySelectorAll("input[name=f]")) i.addEventListener("change",filter);
// A link such as deriva_history.html?q=p76 opens the page already searched for p76.
const asked=new URLSearchParams(location.search).get("q");
if(asked){{ q.value=asked; search(); }} else filter();
</script>
</body></html>
"""

NOTE = {REAL: "Real change", COSMETIC: "Cosmetic change", ADDED: "Added", REMOVED: "Removed"}
BY_HAND, BY_RULE = "checked by hand", "second rule, not checked by hand"


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


def _summary(entries: list[Entry]) -> str:
    """Where the variable changed, for phones: one mark and round per change."""
    parts = [f'<span><i class="dot {e.mark}{" hand" if e.by_hand else ""}"></i>{e.round}</span>'
             for e in entries if e.mark in NOTE]
    return f'<span class="sum">{"".join(parts) or "no change"}</span>'


def _short(text: str, width: int = 70) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 1].rsplit(" ", 1)[0] + "…"


def render(rounds: list[Round], history: dict[str, list[Entry]]) -> str:
    head = []
    for i, r in enumerate(rounds):
        if i and rounds[i - 1].dictionary.layout != r.dictionary.layout:
            head.append('<th class="redesign">redesign<small>not compared</small></th>')
        checked = any(entries[i].by_hand for entries in history.values())
        tick = "some by hand" if checked else ""
        head.append(f"<th>{r.label}<small>{tick}</small></th>")
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
                sheet.append(f'<div class="cutline">Redesign break: the dictionary layout changed in {e.round}, so {e.round} is not compared with the round before</div>')
            # The first round after a redesign is not compared, so it gets no mark at all.
            dot = "missing" if e.text is None or e.mark == BREAK else (e.mark if e.mark in NOTE else "same")
            hand = " hand" if e.by_hand else ""
            who = BY_HAND if e.by_hand else BY_RULE
            if e.mark in (REAL, COSMETIC):
                title = f"{e.round}: {NOTE[e.mark]} ({who})"
            elif e.mark in NOTE:
                title = f"{e.round}: {NOTE[e.mark]}"
            elif e.mark == BREAK:
                title = f"{e.round}: first round after the redesign, not compared"
            else:
                title = e.round
            cells.append(f'<td class="cell"><i class="dot {dot}{hand}" title="{html.escape(title)}"></i></td>')
            if e.text is None:
                text, kind = "Not in this round", "missing"
            elif e.mark in (REAL, COSMETIC) and before is not None:
                text, kind = _diff(before, e.text), e.mark
            else:
                text, kind = html.escape(e.text), e.mark
            who = BY_HAND if e.by_hand else BY_RULE
            note = f'<span class="note">{NOTE[e.mark]}<span class="by">{who}</span></span>' if e.mark in (REAL, COSMETIC) else (
                f'<span class="note">{NOTE[e.mark]}</span>' if e.mark in NOTE else "")
            sheet.append(f'<div class="entry {kind}"><div class="when">{e.round}{note}</div><div class="text">{text}</div></div>')
            before = e.text
        n_cols = len(cells) + 1
        rows.append(
            f'<tr class="row" tabindex="0" aria-expanded="false" data-name="{html.escape(name)}" data-real="{real}" data-changed="{changed}">'
            f'<td class="q"><b>{html.escape(name)}</b><span>{html.escape(_short(latest))}</span>{_summary(entries)}</td>{"".join(cells)}</tr>'
            f'<tr class="detail" hidden><td colspan="{n_cols}"><div class="sheet">{"".join(sheet)}</div></td></tr>'
        )
    hand_total = sum(e.by_hand for entries in history.values() for e in entries)
    steps = [f"{rounds[i - 1].label} and {rounds[i].label}" for i in range(1, len(rounds))
             if any(entries[i].by_hand for entries in history.values())]
    questions = sum(any(e.mark == REAL for e in entries) for entries in history.values())
    changed_vars = sum(any(e.mark in (REAL, COSMETIC, ADDED, REMOVED) for e in entries) for entries in history.values())
    return PAGE.format(
        hand=hand_total, hand_steps=", ".join(steps) or "none",
        first=_month(rounds[0].label), last=rounds[-1].label,
        real=questions, changed_vars=changed_vars, cosmetic=cos_total, n_rounds=len(rounds), variables=len(history),
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
    parser.add_argument(
        "--labels",
        default="eval",
        help="folder with my labels_*.csv files; their labels replace the second rule's (default: eval)",
    )
    args = parser.parse_args(argv)
    try:
        rounds = read_rounds(Path(args.folder))
        labels = Path(args.labels)
        history = build_history(rounds, read_hand_labels(labels) if labels.is_dir() else {})
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
