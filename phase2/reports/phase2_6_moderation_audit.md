# arXiv moderation audit, Phase 2.6 (2026-09-21)

Audit of `phase2/paper/main.tex` at the end of Pass 15, against arXiv's own
moderation criteria over the seven dimensions the pass was asked to cover.
**Nothing here was fixed. By instruction this pass surfaces findings only.**

**The requested skill does not exist.** `arxiv-moderation-check` is not
installed and is not in this session's skill list. Both skill directories
(`~/.claude/skills/`, `.claude/skills/`) and the plugin cache were checked.
The audit below was done directly against arXiv's published criteria, covering
exactly the dimensions asked for. Findings are ranked, not skill-scored.

## Verdict

**No desk-reject risk on content.** Two findings block a first upload, both
mechanical and both cheap. One finding is a decision only the author can take.
The rest are polish.

| # | Finding | Dimension | Severity |
|---|---------|-----------|----------|
| 1 | Commit hashes and artifact paths resolve nowhere public; `phase-2` is unpushed | self-containment | blocking |
| 2 | `\graphicspath{{../reports/figs/}}` escapes the submission directory | format | blocking |
| 3 | No generative-AI disclosure, against a repository that carries AI co-author trailers | disclosure | author decision |
| 4 | `main.bbl` must ship in the tarball; AutoTeX does not run BibTeX | format | high |
| 5 | Abstract is 1,766 of 1,920 allowed characters | metadata | medium |
| 6 | `{,}` digit separators will appear literally in the metadata abstract | metadata | medium |
| 7 | No data or code availability statement; S2AND's ODC-BY licence is never named | rights | medium |
| 8 | cs.LG cross-list is the weakest of the three categories | category fit | low |
| 9 | Short hashes in published text break on any rebase | self-containment | low |
| 10 | No arXiv licence chosen | rights | low, but required at submission |

## 1. Content type and desk-reject risk

**Low.** This is unambiguously a research paper: a formal structural argument,
a pre-registered protocol with a frozen falsification table, a population
accounting table from 766,133 signatures down to the analysis population, five
tables, five figures, a limitations section and seventeen references. It is not
a position piece, a software manual or an unsubstantiated claim, which are the
categories arXiv moderation actually turns away.

Two things a moderator could snag on, neither fatal.

**The paper reports Inconclusive on both selection hypotheses.** Null results
are explicitly welcome on arXiv, and this one does not rest on the null: the
containment result is proven, positive and stated first in the abstract. The
1.2 and 1.4 rewrite in this same pass makes the two halves' different scope
explicit, which helps here as well as with the title.

**Section 8.3 reinterprets the author's own prior work.** A moderator skimming
could read it as a correction to an earlier submission. It is not, and the
prior work is a Zenodo record rather than an arXiv paper, so there is no
replacement or cross-listing question. The section already says in its own
words that it is an interpretation of a published result and not a new
measurement. No change needed; worth knowing if a moderator asks.

**Text overlap with the prior manuscript is effectively zero.** Measured: 1
shared 8-gram between `phase2/paper/main.tex` and `manuscript/main.tex` out of
7,311 in the new paper, and the one hit is a phrase section 8.3 puts in
quotation marks and attributes. Self-citation is one entry of seventeen. No
duplicate-submission or self-plagiarism exposure.

## 2. Category fit

**Primary: cs.DL.** The corpus is bibliographic, the benchmark is an author
name disambiguation benchmark, and the related work sits in digital-library and
bibliometric venues almost without exception: JCDL for S2AND, JASIST for Kim
and Kim, SIGMOD Record for the AND survey, KDD for WhoIsWho, CIKM for Backes.
Author name disambiguation is a core cs.DL topic. The title's "entity
resolution" does not move the paper out of cs.DL, because the substrate is
still the digital library.

**cs.IR as the cross-list, and a defensible alternative primary.** The
mechanisms are a rule and a nearest-neighbour retriever over a string
similarity function, with blocking, so there is real IR content. If the author
would rather be read by an IR audience, cs.IR primary with cs.DL cross-listed
is honest. cs.DL is the better fit on where the work's interlocutors publish.

**cs.LG is the weakest of the three.** The paper contains no learning. Both
mechanisms are untrained lookups by design, and section 1.4 and the limitations
explicitly disclaim any claim about learned systems. What is genuinely cs.LG
adjacent is the algorithm-selection spine (Rice, Smith-Miles, Barbudo) and the
decision-focused-evaluation thread (Hand, Hernandez-Orallo, Vickers and Elkin,
Elmachtoub and Grigas). That is a real connection and a thin one. Requesting it
costs nothing, since moderators reclassify rather than reject over category,
but it is the one most likely to be stripped.

**Consider cs.DB instead of, or beside, cs.LG.** Entity resolution is a
classical database topic and the title uses the database community's term. It
is a closer fit than cs.LG on the strength of the title alone.

Risk on this dimension is reclassification, not rejection.

## 3. Self-containment

**This is the top finding and it is not only a formatting problem.**

Section 6.4 is the paper's pre-registration-integrity argument, the section
STATE.md names as the one that has to survive a reviewer looking for the seam.
It turns on seven short commit hashes in a footnote (`8869b82`, `5e13e38`,
`3d86959`, `c20239a`, `5f452ad`, `3e79a48`, `9e3d921`) and on the phrases "in
the public repository with full history" and "checked at writing against the
committed repository". Table and figure captions name a further fifteen
repository artifacts as their sources.

All 22 were verified to resolve locally in this pass. **None of them resolves
for a reader.** The `phase-2` branch has never been pushed: `origin` carries
only `main`, which is the Phase 1 work. The paper gives no repository URL
anywhere, not in a footnote, not in an availability statement, not in the
bibliography.

As it stands the paper asks readers to take its strongest defence on trust
while pointing at evidence they cannot reach. That is a credibility problem
before it is an arXiv problem.

**There is no data or code availability statement.** The paper says "The
substrate is S2AND" and cites the S2AND paper. That is attribution. It is not
an access route, and the download path recorded in
`phase2/data/MANIFEST_s2and.json` never reaches the manuscript.

**Short hashes will break.** Seven-character hashes in published text do not
survive a rebase, and STATE.md has flagged this since 2.5c. Full hashes, or a
tag, or an archived snapshot with its own DOI, all survive; short hashes do
not.

Shape of the fix, not applied: push `phase-2`, add one availability paragraph
carrying the repository URL and a tag or Zenodo DOI pinning the exact state the
paper describes, and replace the short hashes with full ones or with references
to that pinned state.

## 4. Tone

**Clean. Nothing to fix.**

No promotional language, no priority claims, no disparagement. Kim and Kim
(2020) are treated as the nearest prior work and are credited twice with having
tested the harder comparison, which is the opposite of the usual failure mode.
The self-critical passages, including "a reader is entitled to hold it against
the paper", read as candour rather than as grievance or as false modesty.

Register is plain and direct; the `/anti-ai` pass at 2.5c did its work. Em
dashes are now at zero, per the charter's writing invariants.

Two stylistic notes, neither a moderation matter. The paper narrates its own
process at unusual density ("We did not derive the containment first", "in our
hands", "We found it in an empty cell"). It is earned, because the order of
discovery is load-bearing evidence in section 4.2, but a copyeditor may push
back. And two lines are informal for the register: "This is a trap
practitioners fall into, not a theorem anyone needs" and "permission to stop
deliberating". Both read as deliberate voice.

## 5. Generative-AI disclosure

**A real gap, and the decision is the author's.**

arXiv asks authors to report the use of generative AI tools in their work; AI
tools cannot be listed as authors. The manuscript contains no disclosure of any
kind, not in the acknowledgements, not in a footnote, not in the methods.

The exposure is specific rather than general. The repository's commit history
carries `Co-Authored-By: Claude` trailers, and the paper points readers at that
repository, or will once finding 1 is fixed. A reader who follows the commit
hashes in section 6.4 lands on AI co-authorship trailers that the paper does
not mention. The mismatch is the risk, not the tool use.

This needs a statement of what is actually true about how the work was done,
which is the author's to write and not this pass's to draft. It should be
settled before finding 1 is fixed, since fixing finding 1 is what makes the
commit trailers visible.

## 6. Metadata and format

**Title.** 107 characters, sentence case, no trailing period as of this pass,
no TeX markup. Transfers to the metadata field unchanged. Good.

**Abstract. 1,766 characters against arXiv's 1,920 limit: 154 characters of
headroom.** It will fit, and it will not survive being lengthened. Three
paragraphs, which arXiv accepts.

**The abstract's digit separators will appear literally.** `199{,}713` and
`13{,}902` are LaTeX and the metadata field is plain text. They have to be
retyped as `199,713` and `13,902` when the abstract is pasted into the
submission form, or the braces will show.

**Author field.** Now `Maitreya Sapariya` with a `\thanks` footnote carrying
"Independent researcher" and the ORCID. The ORCID should also be attached to
the arXiv account and author record, not left only in the footnote, so it
propagates to the metadata.

**`\graphicspath{{../reports/figs/}}` is a build blocker.** arXiv unpacks a
submission into a single working directory and runs AutoTeX there. A `../` path
escapes it and the five `\includegraphics` calls will fail. The PNGs must be
shipped inside the submission tree, with the path made relative-downward or
dropped entirely.

**`main.bbl` must be in the tarball.** AutoTeX does not run BibTeX. The file is
generated, and this pass added it to `.gitignore` as a build artifact, which is
right for the repository and means the packaging step has to produce it
explicitly.

**Everything else about the source is AutoTeX-clean.** `article` class at 11pt;
`fontenc`, `inputenc`, `geometry`, `amsmath`, `booktabs`, `graphicx`, `natbib`,
`hyperref`, all standard and all supported. `plainnat` bibliography style. No
custom `.sty`, no journal class. The source is pure ASCII with no non-ASCII
bytes and no stray control characters, verified byte by byte. The PDF is 24
pages and 635 KB, far inside the 10 MB limit.

**Minor.** The five figures are PNG at `width=0.8\linewidth` and will
rasterize; vector PDF would render better at print size. Accepted either way.

## 7. Rights

**S2AND is ODC-BY, and the paper never says so.** The release LICENSE.txt and
README give ODC-BY, recorded with a sha256 in
`phase2/data/MANIFEST_s2and.json`. ODC-BY requires attribution. Citing
`s2and2021` attributes the paper; naming the licence attributes the database.
One sentence in an availability statement covers both, and finding 7 and
finding 1 share a fix.

**The `affiliation` column question is clean for the paper.** S2AND's README
notes that some affiliation data derives from the Microsoft Academic Graph.
The paper uses no affiliation data for any reported number: the signals are
computed from the surname block and the surface form. The raw S2AND JSON under
`phase2/data/raw_s2and/` is gitignored and nothing is redistributed. **This
closes the question for the manuscript. It stays open for any future data
release**, which is how STATE.md flagged it.

**The Kim and Kim preprint PDF is gitignored and not redistributed.** Correct
handling of a publisher preprint with no redistribution licence.

**No third-party figures are reproduced.** All five are generated by
`phase2e_run.py`.

**The prior work's DOIs are internally consistent but not verified against
Zenodo.** `references.bib` gives concept DOI `10.5281/zenodo.21644207`, v1.1.0
at `10.5281/zenodo.22258609` and v1.0.0 at `10.5281/zenodo.21644208`.
`CITATION.cff` gives exactly the same three with the same roles. That is a
cross-check between two local files, not a resolution against Zenodo. **No
network call was made in this pass.** STATE.md's concept-versus-version DOI
item is now narrower but not closed.

**No arXiv licence has been chosen.** One is required at submission: arXiv's
default non-exclusive licence, or CC BY, or CC BY-SA, or CC0. The repository's
MIT licence covers the code and says nothing about the paper text. A decision,
not a defect.

## 8. Endorsement and eligibility

Not one of the seven dimensions asked for, and worth stating because it has the
longest lead time of anything on this list.

A first-time arXiv submitter with no institutional affiliation and no
institutional email will very likely need an endorsement for cs.DL or cs.IR.
Endorsement is per-archive, is requested through arXiv's own flow, and depends
on finding an endorser who has published in that archive. Setting
`\author{}` to "Independent researcher" in this pass makes the question
sharper, not different: it was already true.

**Check this before polishing anything else.** Every other item on this list is
hours of work. This one is not under the author's control and can take weeks.
