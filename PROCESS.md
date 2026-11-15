# Process log

One row per step. Each step is committed.

| Date | Step | What the tool did | What I decided |
|---|---|---|---|
| 2026-11-15 | Start a process log | Created PROCESS.md, added the rule to AGENTS.md so later sessions follow it, logged the decision in PLANNING_LOG.md, committed | After each step: commit and add a row here (step, what the tool did, what I decided) |
| 2026-11-15 | Draft the promo page content | Read README, PLANNING_LOG and eval results; wrote PROMO.md (headline, problem, what it does, evidence, limits, get started) using only numbers already verified in the repo; audience assumed: ENEMDU researchers | Pending: confirm audience and tone |
| 2026-11-15 | Settle promo page decisions | Updated PROMO.md: audience line no longer says "assumed"; Get started now begins with installing uv and cloning https://github.com/esst-prog2/deriva, then cd deriva; nothing else changed | Audience: ENEMDU researchers and analysts working across rounds; English only for now; keep the first person; add install and clone steps |
| 2026-11-15 | Design brief for the promo page | Ran the impeccable shape flow: asked about look, main action and stack; scanned deriva_history.html for local paths and personal data (none found); wrote PRODUCT.md; rolled visual directions and showed them on a decision page; wrote the brief (no code) | New look but keep red dot / grey ring; live demo at docs/history.html after a personal-data check; one static HTML file; direction: The Questionnaire Sheet |
| 2026-11-15 | Link straight to a search on the history page | Added ?q= support to history.py (the page fills the search box from the URL and opens the question when only one matches), added a test (116 passed), checked ?q=p76 in headless Chrome: 1 question shown, p76 opened | Add ?q= with a test so the promo button opens history.html?q=p76; use Google Fonts; brief approved |
