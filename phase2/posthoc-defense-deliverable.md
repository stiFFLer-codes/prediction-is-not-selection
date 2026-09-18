# Writing-phase deliverable: the pre-registration-integrity subsection

Lock this into PLAN.md as a required writing-phase deliverable. It is drafted now,
before 2.2e results exist, on purpose: the argument must not be softened or
strengthened by what the run returns. It goes in the manuscript as a short methods
subsection (working title "Pre-registration and its amendment"), roughly 250 to
350 words, venue-neutral. The bracketed slots are filled at writing time from the
committed repo, not invented.

---

## Draft subsection: pre-registration and its amendment

We pre-registered the hypotheses, the winner definition, the analysis bands, and
the falsification table before computing any evaluation metric, and we froze the
calibration constants in a separate commit before any evaluation number existed
[commit 5e13e38]. The pre-registration and every subsequent amendment are in the
public repository with full history [ref].

We amended the pre-registration once, after two exploratory runs, and we state
that plainly rather than presenting the amended version as the original. The
amendment was forced by two structural facts about the mechanisms, not by an
unwelcome effect size. First, when a test name is present in a block's history it
sits at the maximum of any similarity function, so a single-nearest retriever
returns whatever exact match returns; exact match is therefore a strict sub-case
of single-nearest retrieval, and the two cannot contest a winner. Second, a block
whose history names one author returns that author from any non-empty candidate
pool, so at maximum consistency the only move a mechanism can make is to abstain.
The first fact required replacing the second mechanism with a k-nearest vote that
does not reduce to exact match. The second required scoping the consistency
hypothesis to whether the choice is decidable at all, rather than which mechanism
wins at every consistency level.

Three properties keep the amendment honest. The original hypotheses and the
conditions of the runs that motivated the change remain in the pre-registration,
unedited and dated [ref]. No accuracy figure for the k-nearest mechanism existed
at the time the amended hypotheses were written; the amendment predates the run it
governs [commits: amendment before 2.2e run]. And the one component of the amended
consistency hypothesis that is guaranteed by construction, the decline in decided
winners as consistency approaches its maximum, is labeled as structural wherever
it appears; the empirical content we test lies below that maximum, in the region
where the outcome is not fixed in advance.

---

## Why this is locked now

- It is the single largest threat to the paper's credibility, and it is the exact
  thing the arXiv-moderation and peer-review passes will stress-test.
- Drafting it after results exist would let the outcome shape the argument, which
  is the failure it is meant to prevent.
- If, at writing time, this subsection cannot be made to read as principled rather
  than as rationalization, that is a signal the reframe was weaker than believed,
  and the honest move is to reconsider the paper, not to polish the paragraph.

## Fill-at-writing checklist

- Confirm every [ref] and [commit] against the committed repo before submission.
- Confirm the "amendment predates the run" claim against the actual commit
  timestamps and order (amendment commit before the 2.2e evaluation commit).
- If 2.2e lands H3 as Not supported (gap compression only), this subsection stays
  essentially unchanged; only the framing around it shifts to the honest smaller
  paper. The integrity argument is outcome-independent by design.
