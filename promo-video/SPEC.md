# SPEC: Same name, different question

GOAL:    a stranger leaves knowing that a survey variable can keep its name while its question changes,
         and that deriva shows where; they want to open the promo page.
OUTPUT:  HyperFrames, 1280 x 720, 30 fps, delivered as docs/promo.mp4 (small, H.264).
TIME:    38 s x 30 = 1140 frames (was 30 s; the extra 8 s went to the reading moments: opener, Dec 2020 change + gloss, hand-check table, end card). No beat grid until a music bed is chosen.
LOOK:    the promo page's questionnaire sheet (DESIGN.md), as a medium:
         desk #e6ecf4 ground; sheet #fdfeff inset 32/28 px, shadow 0 18px 48px -20px rgba(18,22,29,.22);
         form ink #2a5bb0 carries every printed structure (rules 1.5 px, number boxes, labels, instruction lines);
         entry ink #12161d carries the questionnaire wording; red #c8102e only on the Dec 2020 real change
         (strike, inserted words, red dot) and the "real change" legend bubble; cosmetic grey #7a8394.
         Display: Archivo (variable file, wdth 85, 700), wording 40 px; instruction lines Archivo italic 28 px form-deep #1c4590;
         field labels Archivo 600 wdth 70 caps 17 px, tracking .08em; rounds and p76 in JetBrains Mono.
         No grain, no vignette: printed form, flat.
OBJECTS: the form header (field cells: Tool, Survey, Variable, Round); the blue question-number box holding p76;
         the wording of p76 as printed; a row of nine answer bubbles, one per round, labelled with the round;
         the hatched band of the 2021 redesign break; the 2x2 hand-check table from Q4 of the promo page.
MOTION:  form is filled in, not faded: words go grey -> ink (0.07 s apart), bubbles fill by a left-to-right
         clip wipe (0.35 s expo.out), rules draw (scaleX, 0.4 s power2.inOut), field values swap by blur swap
         (out 0.15 s, in 0.15 s). Red dot: scale 0.4 -> 1 with back.out(1.6). Camera: one move, the row rising
         to centre (0.7 s power2.inOut). Exits 0.2 s blur + fade.
SHOTS:   0.0-3.0   sheet, header filled (Survey ENEMDU, Variable p76, Round 2019-06), p76 box, wording inks in; "Same name in every round."
         3.0-7.6   Round 2019-12 then 2020-09: month word swaps (MAYO/NOVIEMBRE), grey rings fill bubbles 2 and 3; line -> "Same question?"
         7.6-12.4  Round 2020-12; hold 0.4 s; red strike across "BONO DE DESARROLLO HUMANO?", "BONO o PENSIÓN?" written below, red dot fills bubble 4; line -> "December 2020: a different question."
         12.4-15.4 "deriva" written into the Tool cell; line -> "deriva compares the dictionaries of every round"
         15.4-21.2 wording leaves; the bubble row rises to centre; title "Nine rounds. Every change marked."; break band and bubbles 5-9 fill; legend of the four answers fills
         21.2-25.2 the Q4 table (2021 vs 2025): 9 / 10 / 0 / 3; "22 changes, checked by hand"; punch-in on 0: "Real changes hidden: 0"
         25.2-30.0 "deriva shows what moved. You decide." double rule draws, wordmark + esst-prog2.github.io/deriva, held 2.8 s
BANNED:  dark void; glow; gradients; three cards; everything centred; fade-and-slide-up entrances; titles moving after
         they land; red on anything but the real change; anything that looks like INEC's own forms (no INEC logo,
         no official form codes); first-person "I"/"my"; names of people.
QA:      t=0 (thumbnail reads: p76 + wording), 9.6 (strike + insert + red dot), 13.5 (deriva in Tool cell),
         19.5 (full row + break), 23.5 (0 cell), 29.5 (end card).
