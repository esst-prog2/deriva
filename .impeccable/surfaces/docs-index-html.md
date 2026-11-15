---
version: 1
slug: "docs-index-html"
primary_target: "docs/index.html"
related_targets: ["docs/history.html"]
---

# Surface: promo page (docs/index.html)

Mode: Persuade. Audience: researchers and analysts using ENEMDU across rounds. Action: open the live demo at history.html?q=p76; second, clone and run. Content: PROMO.md verbatim; evidence from eval/result.txt and eval/result_2020_09_vs_2020_12_v2.txt; p76 wordings from deriva-history. Constraints: one static file, inline CSS, little JS, Google Fonts, GitHub Pages main /docs; nothing personal; no INEC logo or look that could pass as an official INEC form.

## Direction contract

THESIS: The page is a printed survey questionnaire about questionnaires: every section is a numbered question the researcher would ask, answered with real data. It refuses the dev-tool landing (headline, terminal screenshot, feature cards).
OWN-WORLD: Cool white sheet, drop-out form blue for all structure (boxes, rules, question numbers, field tints, header band), near-black for entries; red dot = real change and grey ring = cosmetic are the only marks and red is used for nothing else. Archivo across widths (condensed caps for form labels, wide bold for the masthead), JetBrains Mono only for commands and variable names.
STORY: The visitor learns that a variable can keep its name while its question changes (p76), believes deriva because both rules were tested against blind hand labels and never hid a real change, and opens the p76 history or clones the repo.
FIRST VIEWPORT: Form header box with field cells (deriva, module, rounds, source, code link) across the top; Q1 number box beside the headline at about 4.5rem; the instruction line under it; the answer-bubble legend; a skip-arrow line ending in the primary button "Open the history of p76"; a margin column of skip instructions on the right.
FORM: Questionnaire Sheet, my top grounded candidate (pick card, chosen by the user); seed:c0f0a782c31a9c83. Signature: the Q1 bubbles fill once like pencil marks ending on the red dot; skip instructions are real in-page links.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
