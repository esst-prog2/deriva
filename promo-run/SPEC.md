# SPEC: "One run, start to finish"

GOAL:    a stranger with the sound off sees that two survey codebooks go in, a list of
         what changed comes out in seconds, and one question's history can be looked up;
         they leave knowing the command exists and where to get it.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps, silent (the page plays it muted).
TIME:    30.0 s x 30 = 900 frames. No music, no sound.

REAL SCREENS ONLY
- Opening: real excerpts (rows around p76) of four ENEMDU persona dictionaries, each window
  titled with its real file name: enemdu_personas_2019_06.xlsx, enemdu_personas_2020_12.xlsx,
  Diccionario de Datos_persona_anual_2021.xlsx, Diccionario de Datos_persona_anual_2025.xlsx.
- Terminal: the exact stdout of `uv run deriva … 2021 … 2025` and `uv run deriva-history data/`
  (run 2026-11-20), drawn as text in a terminal window. One substitution: the absolute
  output path is shown as `~/deriva/…` so no local path or user name appears.
- Table: the first 13 rows of the real `deriva_2021_vs_2025.csv` (the rows the rule flags real),
  columns as in the file; long cells cut at the column edge, `reason` cut at the window edge.
- Browser: a Chrome screenshot of the generated `deriva_history.html?q=p76` at 1536 px, 2x.
- English glosses and captions are the only added text; the gloss is marked "IN ENGLISH".
- Counts are never stated as fact when they are the rule's: the rule's 13 "real" are called
  "flagged real", next to the 3 that are real by the blind hand check (eval/result.txt).

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
SHOTS:   (scene start-end on the root timeline; times inside a scene are from its start)
  0.0-5.5   intro    caption "Comparing a survey across years?" from frame 0, sub-line "You open
                     every round's codebook, back and forth, to check the question is still the
                     same." 0.45; the four dictionary windows come to the front in turn from 0.55
                     every 0.52 s, p76's row lit each time; captions fade 5.3.
  5.5-14.1  run      caption "Two rounds of a survey. Which questions changed?" + sub-line "The
                     codebooks of Ecuador's employment survey (ENEMDU), 2021 and 2025." from
                     frame 0; command types to 2.6, output prints 2.75; caption "151 variables in
                     2021, 139 in 2025." 3.0 (count lines banded); caption "12 dropped, 22
                     reworded: 13 flagged real, 3 real by hand." 5.6 (removed/cosmetic banded,
                     the `real 13` line in red).
  14.1-20.6 csv      caption "It writes a table: the rule's flag and both wordings, for you to
                     check." 0.05-3.6 (held for reading); rama1 row turns red 3.6 with the caption
                     "Real, checked by hand: the industry classification changed version." and the
                     gloss "IN ENGLISH · rama1: Industry, classification CIIU4 → industry,
                     classification CIIU 4.1 (employed, aged 15+)" 3.72.
  20.6-27.5 history  terminal types `uv run deriva-history data/` to 1.2, prints "9 rounds,
                     190 variables, 11 real changes …" ("11 real changes" banded 1.4); caption "All
                     rounds, 2019 to 2025: 11 real changes in 10 questions." 0.05; browser on p76
                     2.4, blue box on the 2020-12 mark 2.6-3.5; pan 3.6-4.4; caption "Same name,
                     p76. Dec 2020: “Human Development Bonus” became “bonus or pension”." 3.6; red
                     box on the 2020-12 line 4.5.
  27.5-30.0 end      "deriva" wordmark, "See what changed before you compare rounds.",
                     "github.com/esst-prog2/deriva".
BANNED:  dark void ground; glow; gradients; glass; everything centred; fade-and-slide-up on
         everything; text moving while read; logo docked in a corner; mock data of any kind;
         a cursor that clicks things the real page did not need clicking.
QA:      frames 1.0, 4.5 (opening), 6.0 (typing), 9.0, 12.0 (poster), 15.0, 18.5, 22.0, 25.5,
         28.5; every caption at or above its reading floor in `hyperframes check`; phone sheet:
         every caption readable at 360 px.
