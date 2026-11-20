# SPEC: "One run, start to finish"

GOAL:    a stranger with the sound off sees that two survey codebooks go in, a list of
         what changed comes out in seconds, and one question's history can be looked up;
         they leave knowing the command exists and where to get it.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps, silent (the page plays it muted).
TIME:    30.0 s x 30 = 900 frames. No music.

REAL SCREENS ONLY
- Terminal: the exact stdout of `uv run deriva … 2021 … 2025` and `uv run deriva-history data/`
  (run 2026-11-20), drawn as text in a terminal window. One substitution: the absolute
  output path is shown as `~/deriva/…` so no local path or user name appears.
- Table: the first 13 rows of the real `deriva_2021_vs_2025.csv` (the real changes),
  columns as in the file; long cells cut at the column edge, `reason` cut at the window edge.
- Browser: a Chrome screenshot of the generated `deriva_history.html?q=p76` at 1536 px, 2x.
- English glosses and captions are the only added text; glosses are marked "In English".

LOOK:    ground desk #e6ecf4 (flat). Ink #12161d, soft ink #435069. Accent red #c8102e only on
         a real change (the `real` count, the highlighted real rows, the Dec 2020 box).
         Terminal: console #0f1a2e, text #e8eef8, prompt #7f9cd0, highlight band #22324f.
         Table: sheet #fdfeff, rules #a9c0e6, header #edf3fc, real-row tint #fde3e6.
         Gloss strip: #edf3fc with a 6 px #2a5bb0 left rule.
         Caption: Archivo 700, 56 px, -1.5% tracking, left at x=192, top 104; sub-line Archivo
         400 30 px soft ink. Terminal mono: JetBrains Mono 30 px / 44 px lines. Table: Archivo 26 px.
OBJECTS: one window, always in the same place (x 192-1728, y 268-984, 12 px radius, 44 px title
         bar, shadow 0 18 48 rgba(18,22,29,.18)): terminal, then table, then terminal, then browser.
         The window title says what is open (zsh, the CSV file name, the URL).
MOTION:  captions enter by a left-to-right clip wipe, 10 frames, power3.out, and leave by a
         6-frame fade; window contents swap with an 8-frame crossfade; highlight bars grow
         from the left, 9 frames, power2.out; browser pan 24 frames power2.inOut.
         Nothing moves while it is being read.
SHOTS:
  0.0-9.6   run      caption "Two rounds of a survey. Which questions changed?" from frame 0;
                     command types 0.3-3.2; output prints 3.5; caption "151 questions in 2021,
                     139 in 2025." 3.9 (count lines banded); caption "12 dropped, 22 reworded:
                     13 real, 9 cosmetic." 6.6 (removed/cosmetic banded, real in red).
  9.6-20.0  csv      caption "It writes a table: one row per change, both wordings." 0;
                     rama1 row turns red 3.4 + gloss, caption "Real: the industry
                     classification changed version."; p44j row 6.0 + gloss, caption "Just a
                     different spelling of “13th”, still flagged real: deriva errs on the safe side."
  20.0-27.4 history  terminal types `uv run deriva-history data/`, prints; caption "One page with
                     every round, June 2019 to 2025."; 2.0 browser on p76; pan 3.0-3.8; caption
                     "p76 kept its name, but in Dec 2020 “Human Development Bonus” became
                     “bonus or pension”." 3.0; red box on the 2020-12 line 3.9.
  27.4-30.0 end      "deriva" wordmark, "See what changed before you compare rounds.",
                     "github.com/esst-prog2/deriva".
BANNED:  dark void ground; glow; gradients; glass; everything centred; fade-and-slide-up on
         everything; text moving while read; logo docked in a corner; mock data of any kind;
         a cursor that clicks things the real page did not need clicking.
QA:      frames 0.0 (caption + empty prompt), 3.0 (typing), 5.0, 8.0, 12.0, 15.0, 18.5, 21.5,
         25.0, 28.5; phone sheet: every caption readable at 360 px.
