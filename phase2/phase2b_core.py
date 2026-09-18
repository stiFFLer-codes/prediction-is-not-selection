"""Phase 2.2b core: the frozen split, the two signals, the two mechanisms.

Executes `phase2/PREREG.md` sections 3 to 6 and the control definitions of
section 9. Nothing in here is tunable. Every constant below is quoted from the
pre-registration, which was frozen and committed on 2026-09-18 before any
accuracy existed.

What lives here:

- `assign_splits`   PREREG section 3. Calibration/evaluation at block level and
                    train/test inside each block, both at seed 20260918.
- `ads`             PREREG section 5. Train-only purity.
- SV                PREREG section 6. The frozen `surface_variability` from
                    `s2and_blocking.py`, applied to the train half only.
- `canonical_init_form` / `init_share`
                    PREREG section 9. The two Kim and Kim controls: the
                    initialization-canonical surface form behind SV_resid, and
                    INIT.
- `run_block`       PREREG section 4. Exact match and the fuzzy candidate, with
                    the frozen deterministic tie-breaking. The fuzzy cutoff is
                    *not* applied here: the mechanism pass records the best
                    similarity and its candidate, so any cutoff on the frozen
                    grid can be scored from one pass. This is an implementation
                    convenience and changes no definition.
- `block_bootstrap_ci` / `pooled_block_ci` / `verdict`
                    PREREG section 8. The paired per-block bootstrap, the
                    block-resampling pooled bootstrap, and the four-verdict rule.

Run `python phase2/phase2b_core.py` for the self-check.
"""

import re
import sys
import zlib
from pathlib import Path

import numpy as np
import pandas as pd
from rapidfuzz import process as rf_process
from rapidfuzz.distance import JaroWinkler, Levenshtein
from unidecode import unidecode

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from s2and_blocking import surface_variability  # noqa: E402

TABLE = HERE / "data" / "s2and_signatures.parquet"
BLOCKS_CACHE = HERE / "data" / "phase2b_blocks.parquet"
SIGS_CACHE = HERE / "data" / "phase2b_sigs.parquet"

# --- PREREG constants, not tunable -----------------------------------------
SEED = 20260918
CAL_FRACTION = 0.15
BOOTSTRAP_B = 2000
DELTA_PRIMARY = 0.05
DELTAS = (0.05, 0.03, 0.02)          # primary first, then the robustness curve
CUTOFF_GRID = (0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95)
MIN_BLOCKS = 30                      # under-powered below this; never decides
MIN_DATASET_BLOCKS = 100             # a dataset "qualifies" at or above this
ADS_BANDS = ("[0,0.5)", "[0.5,0.7)", "[0.7,0.9)", "[0.9,1.0)", "1.0")
SV_BAND_NAMES = ("SV=0", "SV low", "SV mid", "SV high")
INIT_BANDS = ("INIT=0", "0<INIT<0.5", "INIT>=0.5")
VERDICTS = ("exact wins", "fuzzy wins", "tie", "undecided")
METRICS = {
    "levenshtein": Levenshtein.normalized_similarity,
    "jarowinkler": JaroWinkler.normalized_similarity,
}

NON_LETTER = re.compile(r"[^a-z]+")
INITIAL_ONLY = re.compile(r"^[A-Za-z]\.?$")


def _letters(text):
    """Transliterate to ASCII, lowercase, keep only a-z. Same rule as the key."""
    return NON_LETTER.sub("", unidecode(text or "").lower())


def canonical_init_form(first, middle, last, suffix):
    """PREREG section 9: the initialization-canonical surface form behind SV_resid.

    ASCII, lowercase, letters only; first name reduced to its first letter, each
    whitespace-separated middle token reduced to its first letter, last name and
    suffix kept whole, joined by single spaces. Under this map "John Smith" and
    "J. Smith" are the same string, so forename initialization contributes
    exactly zero to SV_resid.
    """
    parts = [_letters(first)[:1]]
    for token in (middle or "").split():
        parts.append(_letters(token)[:1])
    parts.append(_letters(last))
    parts.append(_letters(suffix))
    return " ".join(p for p in parts if p)


def is_initial_only(first):
    """PREREG section 9: given name is a single ASCII letter, optional period."""
    return bool(INITIAL_ONLY.match((first or "").strip()))


def n_train_for(n):
    """PREREG section 3: n_train = max(1, min(n - 1, floor(0.7 n)))."""
    return max(1, min(n - 1, int(0.7 * n)))


def ads(labels):
    """PREREG section 5: share of signatures belonging to the top author."""
    vals, counts = np.unique(np.asarray(labels), return_counts=True)
    return float(counts.max() / counts.sum())


def init_share(first_values):
    """PREREG section 9: train-only share of initial-only given names."""
    flags = [is_initial_only(f) for f in first_values]
    return float(np.mean(flags)) if flags else float("nan")


def band_seed(label):
    """Deterministic per-analysis seed, PREREG section 8 "same seed scheme".

    Per-block bootstraps use 20260918 + block index, which the pre-registration
    names. A band or cell has no block index, so its offset is a fixed function
    of its label: CRC32, which is stable across runs, platforms and Python
    versions, unlike hash().
    """
    return SEED + int(zlib.crc32(label.encode("utf-8")) % 1_000_000)


# --- the split --------------------------------------------------------------

def assign_splits(sig, verbose=True):
    """PREREG section 3. Returns the signature table with split columns added.

    Block identity is (dataset, block_key), the Phase 2.1 grouping. Blocks are
    ordered by that pair, so `block_index`, which seeds the per-block bootstrap,
    is a property of the data and not of row order.
    """
    sig = sig.sort_values(["dataset", "block_key", "sid"], kind="stable").reset_index(drop=True)
    key = sig["dataset"].astype(str) + "\x00" + sig["block_key"].astype(str)
    codes, uniques = pd.factorize(key, sort=True)
    sig["block_index"] = codes
    sizes = np.bincount(codes, minlength=len(uniques))

    live_mask = sizes >= 2
    live_idx = np.flatnonzero(live_mask)
    n_live = len(live_idx)

    # Calibration split: 15% of live blocks, seed 20260918, block level.
    rng_split = np.random.default_rng(SEED)
    perm = rng_split.permutation(n_live)
    n_cal = int(round(CAL_FRACTION * n_live))
    is_cal = np.zeros(len(uniques), dtype=bool)
    is_cal[live_idx[perm[:n_cal]]] = True

    # Within-block train/test, seed 20260918, blocks visited in sorted order.
    rng_tt = np.random.default_rng(SEED)
    starts = np.zeros(len(uniques) + 1, dtype="int64")
    np.cumsum(sizes, out=starts[1:])
    is_train = np.zeros(len(sig), dtype=bool)
    for b in range(len(uniques)):
        n = sizes[b]
        if n < 2:
            continue
        pos = rng_tt.permutation(n)
        is_train[starts[b] + pos[:n_train_for(n)]] = True

    sig["is_train"] = is_train
    sig["is_live"] = live_mask[codes]
    sig["is_cal"] = is_cal[codes]
    sig["block_size"] = sizes[codes]
    if verbose:
        print("blocks {:,}  live {:,}  calibration {:,} ({:.4%})  evaluation {:,}".format(
            len(uniques), n_live, n_cal, n_cal / n_live, n_live - n_cal))
    return sig


# --- the two mechanisms -----------------------------------------------------

def _form_best_author(forms, labels, block_counts):
    """PREREG section 4 author tie-break, resolved once per distinct train form.

    Most frequent author inside the form, then most frequent inside the block,
    then the lexicographically smallest author id.
    """
    best = {}
    df = pd.DataFrame({"form": forms, "label": labels})
    for form, grp in df.groupby("form", sort=False):
        counts = grp["label"].value_counts()
        cands = sorted(counts.index[counts == counts.max()])
        if len(cands) == 1:
            best[form] = cands[0]
            continue
        top_bc = max(block_counts.get(a, 0) for a in cands)
        best[form] = min(a for a in cands if block_counts.get(a, 0) == top_bc)
    return best


def run_block(train_forms, train_labels, test_forms, simfunc):
    """PREREG section 4: exact match and the fuzzy candidate for one block.

    Returns (exact_pred, fuzzy_pred, fuzzy_sim). Predictions are author ids or
    None for an abstention. `fuzzy_pred` is the candidate *before* the cutoff is
    applied; a caller turns it into the fuzzy mechanism output by abstaining
    wherever `fuzzy_sim < cutoff`.
    """
    block_counts = pd.Series(train_labels).value_counts().to_dict()
    form_counts = pd.Series(train_forms).value_counts().to_dict()
    best_author = _form_best_author(train_forms, train_labels, block_counts)

    # Distinct train forms ordered by the frozen form tie-break: more train
    # signatures first, then lexicographically smallest. argmax takes the first
    # maximum, so this ordering *is* the tie-break.
    ordered = sorted(form_counts, key=lambda f: (-form_counts[f], f))

    distinct_test = sorted(set(test_forms))
    sims = rf_process.cdist(distinct_test, ordered, scorer=simfunc, dtype=np.float32)
    arg = sims.argmax(axis=1)
    best_sim = sims[np.arange(len(distinct_test)), arg]
    per_test_form = {
        f: (best_author[ordered[arg[i]]], float(best_sim[i]))
        for i, f in enumerate(distinct_test)
    }

    exact_pred, fuzzy_pred, fuzzy_sim = [], [], []
    for f in test_forms:
        exact_pred.append(best_author[f] if f in form_counts else None)
        cand, s = per_test_form[f]
        fuzzy_pred.append(cand)
        fuzzy_sim.append(s)
    return exact_pred, fuzzy_pred, np.asarray(fuzzy_sim, dtype=np.float32)


# --- the winner -------------------------------------------------------------

def verdict(lo, hi, delta):
    """PREREG section 8 four mutually exclusive verdicts."""
    if lo > delta:
        return "exact wins"
    if hi < -delta:
        return "fuzzy wins"
    if lo >= -delta and hi <= delta:
        return "tie"
    return "undecided"


def block_bootstrap_ci(n_plus, n_zero, n_minus, seed, B=BOOTSTRAP_B):
    """PREREG section 8: paired per-block bootstrap on d_b = acc_exact - acc_fuzzy.

    Both mechanisms are scored on the same resample, so d_b is the mean of the
    per-signature difference g_i = correct_exact_i - correct_fuzzy_i, which takes
    only the values +1, 0, -1. Resampling signatures with replacement and
    averaging g is therefore exactly a multinomial draw over those three
    categories: identical distribution, O(B) instead of O(B * n_test).
    """
    n = n_plus + n_zero + n_minus
    rng = np.random.default_rng(seed)
    counts = rng.multinomial(n, [n_plus / n, n_zero / n, n_minus / n], size=B)
    d = (counts[:, 0] - counts[:, 2]) / n
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def pooled_block_ci(net, sizes, seed, B=BOOTSTRAP_B, chunk=200):
    """PREREG section 8: pooled band verdict, resampling *blocks* with replacement.

    `net[b]` is (correct_exact - correct_fuzzy) summed over block b test
    signatures; `sizes[b]` is its test-set size. The pooled gap of a resampled
    set of blocks is sum(net) / sum(sizes) over that set, so numerator and
    denominator move together, which is what pooling means.
    """
    net = np.asarray(net, dtype="float64")
    sizes = np.asarray(sizes, dtype="float64")
    m = len(net)
    if m == 0:
        return float("nan"), float("nan"), float("nan")
    point = net.sum() / sizes.sum()
    rng = np.random.default_rng(seed)
    draws = np.empty(B, dtype="float64")
    done = 0
    while done < B:
        k = min(chunk, B - done)
        idx = rng.integers(0, m, size=(k, m))
        draws[done:done + k] = net[idx].sum(axis=1) / sizes[idx].sum(axis=1)
        done += k
    return point, float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def spearman_block_ci(x, y, seed, B=BOOTSTRAP_B):
    """Spearman rho with a block-bootstrap interval (PREREG section 10, H1)."""
    from scipy import stats
    x = np.asarray(x, dtype="float64")
    y = np.asarray(y, dtype="float64")
    point = float(stats.spearmanr(x, y).statistic)
    rng = np.random.default_rng(seed)
    n = len(x)
    draws = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, size=n)
        xb, yb = x[idx], y[idx]
        draws[i] = stats.spearmanr(xb, yb).statistic if xb.std() and yb.std() else np.nan
    draws = draws[~np.isnan(draws)]
    return point, float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def ols_robust(X, y, names):
    """OLS with HC1 standard errors.

    PREREG section 9 asks for block-clustered standard errors on a regression
    whose unit of observation is the block. Each cluster then holds exactly one
    observation, so the cluster-robust estimator reduces algebraically to the
    heteroskedasticity-robust one. That is what is computed here, and the report
    says so rather than printing a "clustered" label that would imply more.
    """
    X = np.asarray(X, dtype="float64")
    y = np.asarray(y, dtype="float64")
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    meat = (X * resid[:, None]).T @ (X * resid[:, None])
    cov = XtX_inv @ meat @ XtX_inv * (n / (n - k))
    se = np.sqrt(np.diag(cov))
    return pd.DataFrame({"term": names, "coef": beta, "se": se, "t": beta / se})


def sv_band_edges(sv_values):
    """PREREG section 6: terciles of the strictly positive SV values."""
    pos = np.asarray([v for v in sv_values
                      if v is not None and not (isinstance(v, float) and np.isnan(v)) and v > 0],
                     dtype="float64")
    return float(np.percentile(pos, 100 / 3)), float(np.percentile(pos, 200 / 3))


def sv_band(value, lo, hi):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    if value == 0.0:
        return SV_BAND_NAMES[0]
    if value < lo:
        return SV_BAND_NAMES[1]
    if value < hi:
        return SV_BAND_NAMES[2]
    return SV_BAND_NAMES[3]


def ads_band(value):
    if value < 0.5:
        return ADS_BANDS[0]
    if value < 0.7:
        return ADS_BANDS[1]
    if value < 0.9:
        return ADS_BANDS[2]
    if value < 1.0:
        return ADS_BANDS[3]
    return ADS_BANDS[4]


def init_band(value):
    if value == 0.0:
        return INIT_BANDS[0]
    if value < 0.5:
        return INIT_BANDS[1]
    return INIT_BANDS[2]


def demo():
    """Self-check. Fails loudly if any PREREG definition drifts."""
    # PREREG section 3 train/test rule, with its own worked examples.
    assert n_train_for(2) == 1
    assert n_train_for(3) == 2
    assert n_train_for(5) == 3
    assert n_train_for(10) == 7
    assert all(n - n_train_for(n) >= 1 for n in range(2, 200)), "every live block keeps a test item"

    # PREREG section 5.
    assert ads(["a", "a", "b"]) == 2 / 3
    assert ads(["a"]) == 1.0

    # PREREG section 9, the SV_resid canonical form: initialization must vanish.
    assert canonical_init_form("John", None, "Smith", None) == "j smith"
    assert canonical_init_form("J.", None, "Smith", None) == "j smith"
    assert canonical_init_form("John", "Quincy", "Smith", None) == "j q smith"
    assert canonical_init_form("J", "Q.", "Smith", "Jr.") == "j q smith jr"
    assert canonical_init_form("Murray", None, "Gell-Mann", None) == "m gellmann"
    assert canonical_init_form("Jurgen", None, "Muller", None) == "j muller"
    # what must survive it: spelling, middle presence, suffix
    assert canonical_init_form("A", "B", "Smith", None) != canonical_init_form("A", None, "Smith", None)
    assert canonical_init_form("A", None, "Smith", "Jr") != canonical_init_form("A", None, "Smith", None)
    assert canonical_init_form("A", None, "Smyth", None) != canonical_init_form("A", None, "Smith", None)
    assert surface_variability({canonical_init_form("John", None, "Smith", None): 1,
                                canonical_init_form("J.", None, "Smith", None): 1}) is None, \
        "identical canonical forms collapse to one key, so no pair remains"

    # PREREG section 9, INIT.
    assert is_initial_only("J") and is_initial_only("J.")
    assert not is_initial_only("John") and not is_initial_only("") and not is_initial_only(None)
    assert not is_initial_only("J.Q."), "two initials is not an initial-only given name"
    assert init_share(["J", "John"]) == 0.5
    assert init_band(0.0) == "INIT=0" and init_band(0.4) == "0<INIT<0.5" and init_band(0.5) == "INIT>=0.5"

    # PREREG section 4, both mechanisms and both tie-breaks.
    tf = ["Jane Smith", "Jane Smith", "J. Smith"]
    tl = ["A", "A", "B"]
    ep, fp, fs = run_block(tf, tl, ["Jane Smith", "Jane Smitn", "Zed Jones"],
                           Levenshtein.normalized_similarity)
    assert ep == ["A", None, None], ep
    assert fp[0] == "A" and fs[0] == 1.0
    assert fp[1] == "A" and 0.8 < fs[1] < 1.0, (fp[1], fs[1])
    # form tie-break: equal similarity, the form with more train signatures wins
    ep2, fp2, fs2 = run_block(["ab", "ab", "cd"], ["A", "A", "B"], ["xy"],
                              Levenshtein.normalized_similarity)
    assert fs2[0] == 0.0 and fp2[0] == "A", (fp2, fs2)
    # author tie-break inside a form: equal form counts -> more frequent in block
    ep3, _, _ = run_block(["ab", "ab", "cd"], ["A", "B", "B"], ["ab"],
                          Levenshtein.normalized_similarity)
    assert ep3 == ["B"], ep3
    # ... then the lexicographically smallest id
    ep4, _, _ = run_block(["ab", "ab"], ["B", "A"], ["ab"], Levenshtein.normalized_similarity)
    assert ep4 == ["A"], ep4

    # PREREG section 8, the four verdicts.
    assert verdict(0.06, 0.20, 0.05) == "exact wins"
    assert verdict(-0.20, -0.06, 0.05) == "fuzzy wins"
    assert verdict(-0.04, 0.04, 0.05) == "tie"
    assert verdict(-0.20, 0.20, 0.05) == "undecided"
    assert verdict(0.04, 0.20, 0.05) == "undecided", "straddling +delta is undecided, not a win"
    assert verdict(-0.05, 0.05, 0.05) == "tie", "the margin is inclusive on the tie side"

    # bootstraps: a block where exact is always right and fuzzy always wrong
    lo, hi = block_bootstrap_ci(10, 0, 0, seed=SEED)
    assert lo == hi == 1.0
    lo, hi = block_bootstrap_ci(0, 10, 0, seed=SEED)
    assert lo == hi == 0.0 and verdict(lo, hi, 0.02) == "tie"
    pt, lo, hi = pooled_block_ci([2, -2, 0], [4, 4, 4], seed=SEED)
    assert pt == 0.0 and lo < 0 < hi

    # pooled gap really is sum(net)/sum(sizes), not a mean of per-block gaps
    pt2, _, _ = pooled_block_ci([1, 0], [1, 99], seed=SEED)
    assert abs(pt2 - 1 / 100) < 1e-12, pt2

    # band helpers
    assert ads_band(0.49) == "[0,0.5)" and ads_band(0.9) == "[0.9,1.0)" and ads_band(1.0) == "1.0"
    assert sv_band(0.0, 0.05, 0.15) == "SV=0"
    assert sv_band(0.04, 0.05, 0.15) == "SV low"
    assert sv_band(0.15, 0.05, 0.15) == "SV high"
    assert sv_band(None, 0.05, 0.15) is None
    lo_e, hi_e = sv_band_edges([0.0, 0.0, 0.1, 0.2, 0.3, None])
    assert 0.1 <= lo_e <= hi_e <= 0.3

    # OLS against a known answer
    rng = np.random.default_rng(0)
    Xd = np.column_stack([np.ones(500), rng.normal(size=500)])
    yd = 1.5 + 2.0 * Xd[:, 1] + rng.normal(scale=0.1, size=500)
    fit = ols_robust(Xd, yd, ["const", "x"])
    assert abs(fit.coef[0] - 1.5) < 0.05 and abs(fit.coef[1] - 2.0) < 0.05, fit

    assert band_seed("a") == band_seed("a") and band_seed("a") != band_seed("b")

    print("phase2b_core self-check: all assertions passed")


if __name__ == "__main__":
    demo()
