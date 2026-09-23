# arXiv moderation audit, Phase 2.8a (2026-09-23)

Re-run of the Phase 2.6 audit (`reports/phase2_6_moderation_audit.md`) against
`phase2/paper/main.tex` as it stands at the end of Pass 21, over the same seven
dimensions. Preceded in the same pass by a contribution-and-moderation scan,
reported first because it is the only part of this audit that changed the
manuscript. **Submission-time items are reported and were not acted on.** The
2.6 file is left as the record of that audit and was not edited.

## Verdict

**No desk-reject risk on content, and the paper now says what it contributes
before page 4.** Nothing on this list blocks a build. One thing still blocks an
upload, and it is the same thing as at 2.6: `phase-2` is unpushed, so the seven
commit hashes in section 6.4 and the availability statement point at a
repository that does not yet contain what the paper says it contains. That is
the release pass's job, not a manuscript edit.

| # | Finding | Dimension | State at 2.8a |
|---|---------|-----------|---------------|
| 1 | No explicit contributions statement; two sentences undersold the structural result | content type | **fixed this pass**, framing only |
| 2 | `phase-2` unpushed; seven hashes and fifteen caption artifacts resolve locally only | self-containment | open, release pass |
| 3 | Availability statement and the locked quote's "public repository" are future-true | self-containment | open, release pass (the quote stays locked; the availability statement moves to present tense after the push) |
| 4 | Short hashes in published text | self-containment | open, release pass: a tag pins them without a rewrite |
| 5 | Two unused PNGs in `paper/figs/` | format | open, release pass; verified droppable (build below) |
| 6 | One `{,}` separator in the abstract will show literally in the metadata field | metadata | open, submission time |
| 7 | Cross-list choice: cs.DB is now better supported than cs.LG | category fit | open, submission time |
| 8 | No arXiv licence chosen | rights | open, submission time |
| 9 | Corresponding address is personal; endorsement for cs.DL not yet requested | eligibility | open, submission time, longest lead |

## The contribution-and-moderation scan

Read as an arXiv moderator assessing a cs submission would read it: is this a
genuine, self-contained research contribution, or a review, survey, opinion
piece or bare negative result?

**It is original research, and it read as one before this pass.** It has a
formal structural argument with a measured confirmation, a pre-registered
protocol with a frozen falsification table, a population accounting from
766,133 signatures down, eight tables, three figures, a limitations section and
25 references. It is not a survey: related work is one section of four
subsections. It is not an opinion piece: every claim points at a committed
number or at an argument stated in full.

**What a skimming moderator could misread, before this pass.** The abstract and
the introduction lead with the honest answer, "mostly no". The positive results
were all present but were stated as reasons the answer is no, not as
contributions, and nowhere did the paper say in one place what it adds. The
methodological cautions, the calibration trap in particular, first appeared in
section 5.2 and were not mentioned in the front matter at all. Two sentences
actively undersold the structural result.

**What changed.** Six framing edits, no claim added, no number new to the paper,
no honesty disclosure touched.

1. **A new section 1.4, "Contributions"**, a four-item list on page 3: the
   structural result and its unreachable-verdict consequence, with the
   AutoBlock precedent conceded inside the item; the pre-registered study on
   real data, with both hypotheses named as Inconclusive; the block-size
   deflation, with "did not pre-register" inside the item; and the cautions for
   portfolio and benchmark design, including the calibration trap. Every
   sentence restates a claim already made in sections 4, 5, 6, 7.7 or 8.2 with
   a pointer to it. The list is not numbered "four" in the text, because
   section 1.3 already speaks of "the four results" and the two sets do not
   map one to one.
2. **Abstract, "a redesigned pair that avoids both problems"** became "a
   redesigned pair in which neither mechanism contains the other". The two
   problems were the nesting and the general form's empty regions, and no pair
   avoids the second: those regions are empty for every pair. The replacement
   is what the two-sidedness counts support.
3. **Section 1.3, the same phrase**, same fix.
4. **Abstract, "Against that, the same statistic predicts each mechanism's own
   accuracy"** became "The consistency statistic, by contrast, predicts". Since
   2.7c the preceding sentences are about block size, so "the same statistic"
   read as block size predicting accuracy at Spearman 0.51 and 0.83, which is
   false. Same word count.
5. **Section 4.3, "a trap practitioners fall into rather than a theorem anyone
   needs"** became "The result is practical rather than deep, and the trap is
   easy to fall into". The concession that the argument is not deep stays; the
   suggestion that nobody needs it goes.
6. **Section 8.1, "separating them is most of what this paper has to offer"**
   became "separating them is the paper's central contribution". Same claim,
   stated as a contribution.

The abstract is 249 words after the edits, inside the 200 to 250 band that
peer-review minor 1 closed at 246. The calibration trap was **not** added to
the abstract: the shortest accurate clause costs about fourteen words and would
reopen minor 1. That is a venue-trim decision, flagged below.

### Flags for human review, not acted on

Each of these would need new analysis or would change a claim rather than its
framing, so by instruction none was made.

- **F1. Section 5.2 overstates the calibration trap for the k-nearest family.**
  It says the accuracy-maximizing protocol, applied to either parameterized
  pair, "selects the degenerate parameter and walks the design straight back
  into a comparison that cannot have a winner". That is exact for the radius
  vote, whose accuracy peaks at r = 0.95 with a rule-side count of 0. On the
  k grid the protocol selects k = 2, which is still two-sided: 181 against 736
  on the calibration split and 987 against 3,990 on evaluation (Table 2). The
  sentence is inherited from `reports/phase2c_pair_design.md` ("would select
  k = 2 or r = 0.95 and walk the design straight back into nesting"). The
  accurate statement is that the protocol moves the parameter toward the
  nested limit in both families, which is how the new contributions item and
  section 8.2 already put it. Correcting 5.2 narrows an existing claim, so it
  is the author's call.
- **F2. The 41% contested-region figure is a calibration-split number.** It is
  quoted in sections 4.3 and 8.4. The evaluation-split equivalent is
  computable from committed records and is what a reader will assume they are
  given (peer-review major 4, closing note). New analysis.
- **F3. The entity resolution width of contribution 1 rests on argument.** Running
  the one-count nesting check on one public non-author-name matching benchmark
  would turn it into a demonstration (peer-review major 4, option 2). New
  experiment, and the paper's own scope paragraph already states the width as
  an argument.
- **F4. The calibration trap is absent from the abstract.** Adding it is about
  fourteen words and takes the abstract to about 263, over the venue band. For
  the venue-specific trim.
- **F5, an option rather than a gap.** Sections 4.1 and 4.3 could be set as a
  stated proposition with a proof. Some cs moderators and reviewers read that
  as the signal of a result. It is a restructuring of section 4 and it moves
  the register away from the author's "practical rather than deep", so it is
  listed and not done.

## 1. Content type and desk-reject risk

**Low, and lower than at 2.6.** Unambiguously a research paper; see the scan
above. The null half is carried by a positive structural result that is stated
first in the abstract and first in the new contributions list.

Self-citation is one entry of 25. Text overlap with the prior manuscript
(`manuscript/main.tex`) was re-measured: 8 shared 8-grams out of 14,277 in the
new paper, every one of them inside section 8.3 and all from two phrases that
describe the earlier study, one in quotation marks and attributed. This pass's
tokenizer is not the one 2.6 used, which is why the count differs from 2.6's
"1 of 7,311"; the location and the attribution are the same. No
duplicate-submission exposure.

Section 8.3's reinterpretation of the author's archived earlier work is
unchanged and still states in its first sentence that the artifact is a Zenodo
record and not a peer-reviewed publication.

## 2. Category fit

**cs.DL primary, cs.IR cross-list, unchanged.** One thing moved since 2.6: the
paper now cites the entity resolution and record-linkage literature
(Fellegi and Sunter, Christen, Papadakis et al., AutoBlock, Mudgal et al.) and
states its structural result at that width in sections 1.2 and 1.3. That makes
**cs.DB a better-supported cross-list than cs.LG**, which the paper still gives
no learning content to support. Submission-time decision, not acted on. Risk on
this dimension is reclassification, never rejection.

## 3. Self-containment

**Still the top finding, and still the release pass's.** The seven hashes in
section 6.4 were re-checked this pass: all resolve on `phase-2`, each is an
ancestor of the branch tip, and their subjects match the roles 6.4 assigns them
(`8869b82` 01:32:56, `5e13e38` 10:46:50, `3d86959` 11:43:11, `c20239a`
12:09:23, `5f452ad` 12:36:16, `3e79a48` 13:04:42, `9e3d921` 14:25:07, all
2026-09-18). None resolves for a reader, because `phase-2` has never been
pushed. The availability statement says "will be public at release", which is
true today and must change to the present tense after the push. The locked
quote's "in the public repository with full history" becomes true at the same
moment; it stays locked and needs no edit.

**One pointer improved this pass.** The H1 figure is back in the paper as
Figure 1, so the text that used to send the reader to
`phase2e_h1_ads_accuracy.png` "in the repository" now cites a figure the reader
has. That old pointer also called the plot a per-block scatter; it is a line
plot of per-band means, and the restored caption says so. The decidability
gradient remains cut and remains a repository pointer in section 7.6.

**The upload bundle.** The build uses three PNGs. `phase2e_decidability_gradient.png`
and `phase2e_k_curve.png` are in `paper/figs/` and unused. An isolated build
with only the three used figures, below, confirms they can be dropped from the
tarball. Whether they stay in the repository is a separate question.

## 4. Tone

**Clean.** No promotional language, no priority claim, no disparagement. The
new contributions list concedes the AutoBlock precedent inside its own first
item rather than leaving it to section 4.3. Zero hits for the AI-tell
vocabulary list in any line added this pass, and zero em dashes in the source
and in the rendered PDF.

The two informal lines 2.6 noted: "a theorem anyone needs" is reframed (scan
edit 5, because it undersold the result, not because of register); "permission
to stop deliberating" in section 8.1 is kept as voice.

## 5. Generative-AI disclosure

**Present, verbatim, unchanged.** It names Claude and the Claude Code agent,
covers planning, code, drafting and revision, and separates how the paper was
made from what it studies. It is consistent with the `Co-Authored-By: Claude`
trailers a reader will find in the repository after the push, including this
pass's commit. Nothing to do.

## 6. Metadata and format

- **Title.** 113 characters, sentence case, no TeX markup, no trailing period.
  Transfers to the metadata field unchanged.
- **Abstract.** 249 words; **1,565 characters** with the separator retyped,
  against arXiv's 1,920, so 355 of headroom. One paragraph.
- **One `{,}` separator** in the abstract (`199{,}713`). Retype it as
  `199,713` in the metadata field. Submission time.
- **Build.** Clean `pdflatex`, `bibtex`, `pdflatex` x3: 27 pages, zero undefined
  citations, zero undefined references, zero LaTeX warnings, 25 `\bibitem`s.
  Four underfull-box notices, all cosmetic (two in the affiliation footnote,
  one bibliography line, one body line); no overfull boxes.
- **AutoTeX simulation.** `main.tex`, `main.bbl` and the three used PNGs alone
  in an empty directory, two `pdflatex` runs and no BibTeX: zero undefined,
  zero warnings, zero missing files, 27 pages, 590 KB.
- **`main.bbl`** regenerated this pass and committed; it must go in the
  tarball because AutoTeX does not run BibTeX. No "Unverified" string survives
  in it or in the PDF.
- **Source.** `main.tex` and `references.bib` are pure ASCII, no control
  characters, verified byte by byte.
- **ORCID** is in the `\thanks` footnote; attach it to the arXiv account too, so
  it reaches the metadata. Submission time.

## 7. Rights

**Unchanged from 2.6b.** S2AND's ODC-BY licence is named and nothing is
redistributed. All three figures are generated by the project's own
`phase2e_run.py`; no third-party figure or table is reproduced. The eight
Block E entries are bibliographic metadata only. **No arXiv licence is chosen
yet**; one is required at submission (arXiv's non-exclusive default, CC BY,
CC BY-SA or CC0). The repository's MIT licence covers the code and not the text.

## Eligibility, carried over

Not one of the seven dimensions, and the longest-lead item on the list. The
corresponding address is a personal Gmail account, which is fine in print but
forecloses arXiv's automatic endorsement route. Registering an `adit.ac.in` or
`cvmu.edu.in` address with the arXiv account, then opening the cs.DL
endorsement request, is still the first thing to start.
