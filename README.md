# deriva

Compares the variable dictionaries of two survey rounds and reports what changed
in the instrument between them.

## 1. The demo

I open a terminal and run `deriva enemdu_2019_diciembre.xlsx enemdu_2024_diciembre.xlsx`.
It prints about [N] differences grouped by type: [n] new variables, [n] that disappeared,
[n] whose response categories changed, [n] renamed but with the same question text.
I open the CSV it wrote next to the files, and each row has the variable name in each
round, the question text in each round, the type of change, and the reason it was
classified that way. The last block lists the [n] variables it could not match with
confidence, for manual review. Then I run it on two consecutive rounds, 2023 and 2024,
and it reports [n] changes — the point being that it does not invent differences where
the instrument stayed still.

## 2. The shape

```
in           two ENEMDU variable dictionaries (Excel), one per round
out          a printed summary by type of change + a CSV, one row per change
in between   read each dictionary into a list of variables with question text and
             response categories; match variables across rounds by name first, then
             by question text for the ones left over; classify each matched pair as
             unchanged, renamed, reworded or recategorised; report what stayed unmatched
```

## 3. The size

The first useful version:

- takes two dictionary files as command-line arguments
- reads variable name, question text and response categories out of each
- matches variables across rounds by name, and by question text where the names differ
- classifies every variable as new, removed, renamed, reworded, recategorised or unchanged
- prints counts by type and writes one CSV with a row per change and the reason for it
- lists variables it could not match, instead of forcing a pair

Explicitly not this term:

- reading the microdata itself — only the dictionary
- deciding whether two variables are *comparable for analysis*; that is a judgement the
  researcher makes, and the tool only shows what moved
- harmonising or recoding the data so rounds can be pooled
- comparing more than two rounds in one run
- a graphical interface
- dictionaries from other surveys; the reader is written for the ENEMDU layout first
- learned matching of any kind; a text similarity threshold I can explain is enough

## 4. How we would know it works

- Given a dictionary file whose sheet has no variable-name column, it exits with an error
  naming the column it could not find.
- Given the same dictionary compared against itself, it reports zero changes and zero
  unmatched variables.
- Given a variable that keeps its question text but changes name between rounds, it appears
  once as renamed, not as one removed plus one new.

## 5. What could stop this

The dictionaries are published as Excel, but the layout is not identical across rounds —
headers sit in different rows, columns get renamed, cells are merged. Some rounds may be
published only as PDF; those are out of scope, and if that turns out to be most rounds
the project shrinks to the years that are readable.

Matching by question text is the part I have not built before. The same question is not
always written the same way twice — accents, capitalisation, a trailing instruction — so
the matcher can pair the wrong things or refuse to pair the right ones. My answer to that
is the unmatched list: when the tool is unsure it says so instead of guessing.

Response categories are sometimes stored as free text in a single cell rather than as
separate rows, which makes "the categories changed" harder to detect than "the wording
changed".

The data is ENEMDU, the Ecuadorian national employment survey. It is public microdata
published by INEC through its national data archive, free to download and free to show in
class, so the demo files can live in the repository. ENEMDU is also the honest test case:
the rounds really do differ, so the tool has something to find. The instrument I most want
to point it at afterwards is not public, which is another reason the demo runs on ENEMDU.
