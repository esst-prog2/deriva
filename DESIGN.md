---
name: deriva
description: A printed survey questionnaire about questionnaires; drop-out form blue structure on a cool white sheet, with one red mark that means a real change.
colors:
  form-blue: "#2a5bb0"
  form-blue-deep: "#1c4590"
  form-line: "#a9c0e6"
  form-tint: "#edf3fc"
  band-deck: "#e3ebfa"
  band-instruction: "#d4e1f7"
  band-margin: "#dfe8f8"
  real-red: "#c8102e"
  real-tint: "#fdf2f3"
  real-highlight: "#fde3e6"
  cosmetic-grey: "#7a8394"
  ink: "#12161d"
  ink-soft: "#435069"
  sheet: "#fdfeff"
  desk: "#e6ecf4"
  selection: "#cfe0fb"
  console: "#0f1a2e"
  console-text: "#e8eef8"
  console-prompt: "#7f9cd0"
  console-raised: "#22324f"
  console-edge: "#3a4d70"
typography:
  wordmark:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "2rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontVariation: "\"wdth\" 125"
  display:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.6rem, 6.4vw, 5.5rem)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.03em"
    fontVariation: "\"wdth\" 80"
  headline:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.9rem, 3.8vw, 3rem)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.025em"
    fontVariation: "\"wdth\" 80"
  title:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 700
    lineHeight: 1.25
    fontVariation: "\"wdth\" 85"
  instruction:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.1rem"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
    fontVariation: "\"wdth\" 100"
  label:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.7rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.08em"
    fontVariation: "\"wdth\" 70"
  numeral:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "2.1rem"
    fontWeight: 700
    lineHeight: 1
    fontFeature: "\"tnum\""
    fontVariation: "\"wdth\" 80"
  mono:
    fontFamily: "JetBrains Mono, ui-monospace, Menlo, monospace"
    fontSize: "0.92rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  none: "0px"
  hairline: "2px"
  bubble: "50%"
spacing:
  xs: "0.4rem"
  sm: "0.75rem"
  md: "1rem"
  lg: "1.5rem"
  xl: "2rem"
  gutter: "clamp(1rem, 4vw, 3.5rem)"
  question: "clamp(2rem, 4vw, 3rem)"
components:
  button-primary:
    backgroundColor: "{colors.form-blue}"
    textColor: "{colors.sheet}"
    rounded: "{rounded.hairline}"
    padding: "0.8rem 1.3rem"
    typography: "{typography.title}"
  button-primary-hover:
    backgroundColor: "{colors.form-blue-deep}"
    textColor: "{colors.sheet}"
  question-number:
    backgroundColor: "{colors.form-blue}"
    textColor: "{colors.sheet}"
    rounded: "{rounded.none}"
    size: "4.75rem"
    typography: "{typography.numeral}"
  sub-number:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.form-blue}"
    rounded: "{rounded.none}"
    size: "2.25rem"
  form-cell:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.55rem 0.8rem 0.7rem"
  form-cell-lead:
    backgroundColor: "{colors.form-tint}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.55rem 0.8rem 0.7rem"
  command-block:
    backgroundColor: "{colors.console}"
    textColor: "{colors.console-text}"
    rounded: "{rounded.hairline}"
    padding: "1rem 6.5rem 1rem 1.1rem"
    typography: "{typography.mono}"
  copy-button:
    backgroundColor: "{colors.console-raised}"
    textColor: "{colors.console-text}"
    rounded: "{rounded.hairline}"
    padding: "0.5rem 0.7rem"
  copy-button-done:
    backgroundColor: "{colors.console-text}"
    textColor: "{colors.console}"
  mark-real:
    backgroundColor: "{colors.real-red}"
    rounded: "{rounded.bubble}"
    size: "1.05rem"
  mark-cosmetic:
    backgroundColor: "{colors.sheet}"
    rounded: "{rounded.bubble}"
    size: "1.05rem"
---

# Design System: deriva

## Overview

**Creative North Star: "The Questionnaire Sheet"**

The promo page is a printed survey questionnaire about questionnaires. A single cool white sheet sits on a pale blue desk; everything printed on it in advance (boxes, rules, question numbers, field labels, tints, arrows) is in drop-out form blue, the ink a scanner is meant to ignore, and everything that is an answer or an entry is near-black. Sections are numbered questions with a filled number box on the left, a body in the middle and a margin column of skip instructions on the right that are real in-page links.

The system is flat, ruled and square. Depth is the sheet lifting off the desk and nothing else. Colour carries meaning, not decoration: blue is the form, black is what was written on it, and red is reserved for exactly one thing, a real change in a question's wording. Archivo is the only text face, worked across its width axis: condensed caps for form labels, a wide heavy cut for the wordmark, a slightly narrowed bold for questions. JetBrains Mono appears only where the reader would type or recognise a literal: commands and variable names.

This page is a different visual world from the generated history page (`docs/history.html`), which keeps its own older look. The two surfaces share only the mark meanings: red dot = real change, grey ring = cosmetic change, an outer black ring = checked by hand, and a hatched band = the 2021 redesign break.

**Key Characteristics:**
- One sheet, one form ink (blue), one entry ink (near-black), one meaning-bearing accent (red).
- Square corners everywhere except answer bubbles (circles) and a 2px hairline on buttons and command blocks.
- Structure is drawn with rules and boxes (1.5px form-blue rules, 1px light form lines), never with cards or shadows.
- Archivo's width axis does the typographic work; size and weight stay in a narrow band.
- Every section reads as a numbered question with a margin of skip instructions.

## Colors

A drop-out form palette: cool, pale blues for everything printed, near-black for entries, and one red that is a verdict, not a colour.

### Primary
- **Drop-out Form Blue** (form-blue): every printed structure. Question number boxes, header and section rules, table heads, field labels, sub-question and step boxes, the skip-route arrow, the primary button, focus outlines.
- **Deep Form Blue** (form-blue-deep): the same ink where it must read as text: links, italic instruction lines, skip-margin text, button hover.
- **Form Line** (form-line): the light ruling. Internal cell dividers, table row rules, tally-grid borders, the empty bubble outline.
- **Field Tint** (form-tint): the pre-printed fill of a field. The lead header cell, agreeing tally cells, the hatch colour of the break band.
- **Band tones** (band-deck, band-instruction, band-margin): pale blues for text set on the question 1 band: the line under the headline, the italic instruction and the skip margin. Only on the band.

### Secondary
- **Real-change Red** (real-red): the red dot, the red underline under inserted wording, the "real" verdict text, the favicon. Nothing else.
- **Real Row Tint** (real-tint) and **Inserted Wording Highlight** (real-highlight): the faint wash behind a row that really changed and the marker behind the words that changed in it. Both exist only in service of the red dot.

### Neutral
- **Entry Ink** (ink): body text, headlines, entries in the header cells, the hand-check ring, the verdict rule.
- **Soft Ink** (ink-soft): secondary entries, round codes, table notes, footer text.
- **Cosmetic Grey** (cosmetic-grey): the thick grey ring that means a cosmetic change.
- **Sheet** (sheet): the page surface and the text colour on filled form-blue boxes.
- **Desk** (desk): what the sheet lies on; also the scrollbar track.
- **Selection** (selection): text selection on the sheet.
- **Console family** (console, console-text, console-prompt, console-raised, console-edge): the dark command blocks and their copy button, a navy derived from the form blue rather than a neutral black.

### Named Rules
**The One Red Rule.** Real-change red marks a real change in a question's wording and is used for nothing else: not for errors, emphasis, buttons, links or hover states. Its tints exist only around a red dot.

**The Drop-out Ink Rule.** Anything printed before the reader arrives (structure, labels, numbers, instructions, navigation) is form blue; anything that is data or an answer is ink. If an element is blue, it must be part of the form.

## Typography

**Display Font:** Archivo (variable, width 62 to 125), with Helvetica Neue, Arial
**Body Font:** Archivo, same stack
**Label/Mono Font:** JetBrains Mono (400, 600), with ui-monospace, Menlo

**Character:** One grotesque stretched to play every part a printed form needs: condensed caps for field labels, a wide black wordmark like a form title, narrowed bold for the questions. The mono is a literal, not a style.

### Hierarchy
- **Wordmark** (800, 2rem, width 125, line-height 1, tracking -0.02em): "deriva" in the lead header cell only, always lowercase.
- **Display** (700, clamp 2.6rem to 5.5rem, width 80, line-height 1.02, tracking -0.03em, max 15ch): the question 1 headline, sheet-white on the form-blue band. The line under it is semibold, clamp 1.35rem to 2rem, in band-deck.
- **Headline** (700, clamp 1.9rem to 3rem, width 80, line-height 1.12, max 20ch): every later question, phrased as a question.
- **Title** (700, 1.2rem, width 85): sub-question heads and tally heads (1.05rem there).
- **Instruction** (400 italic, 1.1rem, form-blue-deep, max 62ch): the instruction line under a question, as on a printed form.
- **Body** (400, 1.0625rem, line-height 1.6, max 68ch; 1rem below 40rem): running text.
- **Label** (600, 0.7rem, width 70, uppercase, tracking 0.08em, form blue): field labels in the header, table column heads, tally-grid heads.
- **Numeral** (700, 2.1rem, width 80, tabular): question numbers, sub-question letters and step counters (0.95rem in the small boxes), tally counts (2.1rem).
- **Mono** (400, 0.92rem in command blocks, 0.9em inline): commands, file names, variable names such as `p76`.

### Named Rules
**The Width Axis Rule.** Hierarchy is expressed through Archivo's width axis first (70 for labels, 80 for numerals, 85 for questions, 100 for text, 125 for the wordmark), weight second, size last. Do not add a second sans.

**The Literal Mono Rule.** JetBrains Mono is only for text the reader could type or search: commands, variable names, round codes. Never for labels or decoration.

## Layout

A single centred sheet (max 76rem) on the desk, with a fluid gutter (clamp 1rem to 3.5rem) and top margin that collapses to zero on phones. The sheet opens with a form header: a bordered row of five field cells (lead cell tinted, holding the wordmark), followed by the questions.

Each question is a three-column grid: a 4.75rem number box, a flexible body, and a 13rem margin of skip instructions, separated by a fluid column gap (1rem to 2rem). Questions are separated by a 3px form-blue rule and padded vertically by clamp 2rem to 3rem. Text measure is capped at 62 to 68ch.

Question 1 is a full-bleed form-blue band (to the sheet edges, padded by the gutter) holding the number box (inverted: sheet fill, blue numeral), the headline, the line under it, the instruction and the skip margin. Its answer (legend, button, film) follows on the sheet, aligned to the question body column.

Responsive: at 64rem the header becomes two columns (lead cell full width) and the skip margin drops below the body, aligned to the body column. At 40rem everything is one column, the number box shrinks to 3.25rem and sits above the heading, the tallies stack, the "change" column of the history table hides, the skip-route line hides, and the sheet loses its shadow. Spacing within a question runs on 0.4 / 0.75 / 1 / 1.5 / 2rem.

## Elevation & Depth

Flat by default. The only shadow in the system is the sheet itself lifting off the desk (a 1px contact shadow plus a long soft drop), which is removed on phones where the sheet fills the screen. Inside the sheet, depth is never used: hierarchy comes from rules, boxes, tints and ink weight. The hand-check ring on a mark is drawn with a box-shadow but reads as a printed ring, not elevation.

### Shadow Vocabulary
- **Sheet lift** (`box-shadow: 0 1px 2px rgba(18,22,29,.06), 0 18px 48px -20px rgba(18,22,29,.22)`): the sheet on the desk. Only there.
- **Hand-check ring** (`box-shadow: 0 0 0 3px var(--sheet), 0 0 0 4.5px var(--ink)`): an outer ink ring around a mark that was checked by hand.

### Named Rules
**The One Sheet Rule.** There is one raised surface, the sheet. Nothing on it floats: no cards, no lifted panels, no hover elevation. The question 1 band is printed form ink, not a raised surface: flat, no shadow.

## Shapes

Square, ruled form geometry. Boxes, cells, number boxes, checkboxes and tally cells have square corners; rules are 1.5px form blue for structure and 1px form-line for subdivisions, with a 2.5px ink border reserved for the one tally cell that matters (real changes hidden). The footer closes the form with a 3px double rule. The only circles are answer bubbles. The only rounding is a 2px hairline on the primary button, command blocks and copy button. The 2021 redesign break is a band hatched at 135 degrees (6px sheet, 2px field tint) across the full table width.

## Components

### Buttons
Restrained and printed: a filled form-blue bar, not a pill.
- **Shape:** near-square (2px radius).
- **Primary:** form-blue fill, sheet-white text, Archivo 600 at 1.05rem, padding 0.8rem 1.3rem, a trailing arrow icon drawn as an inline stroked SVG.
- **Hover / Focus:** fill deepens to form-blue-deep over 0.2s on an ease-out curve; focus is a 2px form-blue outline offset 3px (global).
- **Approach route:** on the first question the button is reached by a 1.5px form-blue skip-route line ending in a solid triangle, preceded by a deep-blue lead-in phrase; a full-width secondary text link follows below.

### Answer Bubbles (signature)
The legend and every mark in the system.
- **Real:** a 1.05rem circle with a red rim and solid red fill.
- **Cosmetic:** the same circle with a thick (2.5px) grey ring and no fill.
- **Added / removed:** a short 2px ink dash in place of a bubble.
- **Checked by hand:** any mark wrapped in a 3px sheet gap and a 1.5px ink ring.
- **Motion:** in the question 1 legend, marks fill left to right like pencil strokes (clip-path wipe, 0.5s, staggered 0 / 0.25 / 0.5 / 0.9s, ending on the red dot); the cosmetic ring fades in from form-line. Only when reduced motion is not requested.
- **Codes:** each legend answer carries a condensed form-blue answer code (1 to 4), as on a coded questionnaire.

### Form Header
- **Style:** a 1.5px form-blue box of field cells divided by 1px form-line; each cell is a condensed caps label over an ink entry (0.95rem, 500). The lead cell is tinted and holds the wordmark.

### Question Block
- **Number box:** solid form-blue square (4.75rem), sheet-white tabular numeral; inverted on the question 1 band.
- **Sub-questions and steps:** outlined form-blue squares (2.25rem) with a blue letter or counter.
- **Skip margin:** deep-blue 0.9rem text; its link is bold with a leading arrow icon and points to a real anchor.

### Data Tables
- **Wording history:** caption in condensed form blue; caps column heads over a 1.5px form-blue rule; rows divided by form-line. A real-change row gets the real tint, red verdict text, and the changed words marked with the highlight plus a 2px red underline. Round codes are mono in soft ink.
- **Break band:** a full-width hatched row with italic deep-blue text stating the break.
- **Tally grid:** a 2 by 2 agreement grid with form-line cell borders, tinted agreeing cells, 1.6rem bold counts, and the "real hidden" cell outlined in 2.5px ink with a caps sublabel.

### Command Block
- **Style:** console navy with pale text, 2px radius, mono 0.92rem with wrapping lines; prompts in a muted blue and not selectable; selection in form blue.
- **Copy button:** top-right, 0.8rem Archivo 600 on a raised navy with a navy edge; hover lightens; on success it inverts (pale fill, navy text) and reads "Copied" for about two seconds. On phones it sits above the first line.

### Lists
- **Facts:** small solid form-blue squares as bullets.
- **Not done:** empty outlined form-blue checkboxes, left blank on purpose.
- **Verdict:** a 1.5rem semibold statement under a 3px ink rule.

## Do's and Don'ts

### Do:
- **Do** draw every printed structure (rules, boxes, labels, numbers, arrows, instructions) in form blue and every entry in ink.
- **Do** keep red for real changes only, with its row tint and highlight only around a red dot.
- **Do** use the shared marks exactly: red dot = real, grey ring = cosmetic, outer ink ring = checked by hand, hatched band = 2021 redesign break.
- **Do** structure new sections as numbered questions with a number box and, where it helps, a skip instruction that is a real link.
- **Do** vary Archivo's width axis (70 / 80 / 85 / 100 / 125) before reaching for a new size or weight.
- **Do** keep corners square, with the 2px hairline only on buttons and command blocks.

### Don't:
- **Don't** use red for errors, emphasis, links, buttons or hover.
- **Don't** add cards, lifted panels or shadows inside the sheet; the sheet is the only raised surface.
- **Don't** set labels or decoration in JetBrains Mono; mono is for literals.
- **Don't** introduce a second sans or a serif.
- **Don't** imitate an official INEC form, logo or letterhead; the page borrows the grammar of a questionnaire, not an institution's identity.
- **Don't** port this look onto the history page by assumption; it keeps its own look and shares only the marks.
