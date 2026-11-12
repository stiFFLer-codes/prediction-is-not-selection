"""Phase 2.9b step 1: per-population verdicts, the INIT control cells, and the
Experiment 1 interval count.

A supplementary analysis on records that already exist, in the conventions of
`phase2_9a_matched.py`. Nothing is re-run, re-tuned, re-banded or redefined: the
per-block records are `reports/tables/phase2e_blocks_scored.csv.gz`, the pooled
verdict is the frozen `phase2e_run.pooled_table` at `PRIMARY`, the structural
outcome is the frozen `phase2e_run.structural`, the populations are the frozen
`phase2b_run.populations`. Sub-population intervals use new seeds, tagged
`p29b|<population>|<axis>`, so only their point gaps can be checked against the
committed tables, and they are.

Before anything is computed, `phase2_9a_matched.load` re-derives the frozen
primary population (13,902 blocks, 197,479 test signatures, rule 0.824442, k-NN
0.829440) and halts if any of the four differs.

Outputs (reports/tables/):
1. phase2_9b_population_verdicts.csv  Whole-population pooled gap, interval and
   verdicts at the three margins, for the frozen ten populations plus
   `non-inspire without kisti`.
2. phase2_9b_bands_by_population.csv  The same by ADS band and by SV band.
3. phase2_9b_cells_by_population.csv  The same over the 5 by 4 ADS-by-SV grid.
4. phase2_9b_structure_by_population.csv  Winner reversal, tie-crossing or gap
   compression, across SV at fixed ADS and across ADS at fixed SV, three margins.
5. phase2_9b_init.csv  The INIT control: by INIT band alone, and for the two
   INIT-by-SV cells decided at delta = 0.05, test signatures by dataset and the
   cell with each dataset left out in turn.
6. phase2_9b_exp1_clean_intervals.csv  The 120 clean Experiment 1 conditions, read
   from the `v1.1.0` tag object, with whether the paired-difference interval lies
   inside +-0.02.
Every table carries rule-right-vote-wrong and vote-right-rule-wrong counts where
it has blocks. The report `reports/phase2_9b_report.md` is regenerated from the
run; its hand-written last section is kept as it is.

Run: python phase2/phase2_9b_supplement.py
"""

import contextlib
import io
import platform
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from phase2b_core import ADS_BANDS, DELTAS, INIT_BANDS, SV_BAND_NAMES  # noqa: E402
from phase2b_run import TABLES, dump, md_table, populations  # noqa: E402
from phase2e_run import DECIDED, PRIMARY, order_bands, pooled_table, sort_cells, structural  # noqa: E402
from phase2_9a_matched import load, versions  # noqa: E402

REPORT = HERE / "reports" / "phase2_9b_report.md"
HAND = "## Local file times for the 2.2e run"
EXP1 = "data/outputs/experiments/exp1/final/final_condition_results.csv"
EXP1_MARGIN = 0.02
PLUS, MINUS = "n_plus_" + PRIMARY, "n_minus_" + PRIMARY
COUNTS = {PLUS: "rule_right_vote_wrong", MINUS: "vote_right_rule_wrong"}
# the two cells of phase2e_pooled_init_sv.csv decided at delta = 0.05 (master plan W1)
INIT_CELLS = {("INIT=0", "SV high"): "rule wins", ("INIT>=0.5", "SV=0"): "k-NN wins"}
SHOW = ["n_blocks", "n_test", "pooled_gap", "ci_lo", "ci_hi", "verdict_0.05", "verdict_0.03",
        "verdict_0.02", "under_powered", "rule_right_vote_wrong", "vote_right_rule_wrong"]


def table(g, keys, tag):
    """The frozen pooled table plus the two disagreement counts per group."""
    t = pooled_table(g, keys, PRIMARY, tag)
    s = g.groupby(keys)[[PLUS, MINUS]].sum().reset_index().rename(columns=COUNTS)
    return t.merge(s, on=keys, how="left", validate="one_to_one")


def whole(g, tag):
    """One row for the whole of `g`, labelled `tag|whole` for its seed."""
    return table(g.assign(scope="whole"), ["scope"], tag).drop(columns="scope")


def all_pops(bk):
    pops = populations(bk)
    return pops + [("non-inspire without kisti", bk[~bk.dataset.isin(["inspire", "kisti"])])]


def task_a(bk):
    whl, bands, cells, struct = [], [], [], []
    for name, g in all_pops(bk):
        whl.append(whole(g, "p29b|" + name).assign(population=name))
        for axis, col, order in (("ads", "ads_band", ADS_BANDS), ("sv", "sv_band", SV_BAND_NAMES)):
            t = order_bands(table(g, [col], "p29b|{}|{}".format(name, axis)), col, order)
            bands.append(t.rename(columns={col: "band"}).assign(population=name, axis=col))
        c = sort_cells(table(g, ["ads_band", "sv_band"], "p29b|{}|cells".format(name)))
        cells.append(c.assign(population=name))
        for d in DELTAS:
            for fixed, vary, order, label in (("ads_band", "sv_band", SV_BAND_NAMES, "across SV at fixed ADS"),
                                              ("sv_band", "ads_band", ADS_BANDS, "across ADS at fixed SV")):
                s = structural(c, fixed, vary, order, d).rename(columns={fixed: "fixed_level"})
                struct.append(s.assign(population=name, direction=label, delta=d))
    first = lambda df, cols: df[cols + [x for x in df.columns if x not in cols]]  # noqa: E731
    return (first(pd.concat(whl, ignore_index=True), ["population"]),
            first(pd.concat(bands, ignore_index=True), ["population", "axis", "band"]),
            first(pd.concat(cells, ignore_index=True), ["population", "ads_band", "sv_band"]),
            first(pd.concat(struct, ignore_index=True), ["population", "direction", "delta", "fixed_level"]))


def check_against_committed(whl, bands, cells):
    """The `all` rows reproduce the committed point gaps; every population its gap."""
    allp = "all (primary population)"
    pairs = [(bands[(bands.population == allp) & (bands.axis == "ads_band")].rename(columns={"band": "ads_band"}),
              "phase2e_pooled_ads.csv", ["ads_band"]),
             (bands[(bands.population == allp) & (bands.axis == "sv_band")].rename(columns={"band": "sv_band"}),
              "phase2e_pooled_sv.csv", ["sv_band"]),
             (cells[cells.population == allp], "phase2e_pooled_cells_sv.csv", ["ads_band", "sv_band"])]
    flips = 0
    for mine, name, keys in pairs:
        ref = pd.read_csv(TABLES / name)
        m = mine.merge(ref, on=keys, suffixes=("", "_ref"), validate="one_to_one")
        assert len(m) == len(ref) == len(mine), (name, len(m), len(ref), len(mine))
        assert ((m.pooled_gap - m.pooled_gap_ref).abs() < 1e-12).all(), name
        assert (m.n_blocks == m.n_blocks_ref).all() and (m.n_test == m.n_test_ref).all(), name
        flips += sum(int((m["verdict_{:.2f}".format(d)] != m["verdict_{:.2f}_ref".format(d)]).sum())
                     for d in DELTAS)
    acc = pd.read_csv(TABLES / "phase2e_accuracy_by_population.csv").set_index("population")
    for r in whl.itertuples(index=False):
        if r.population in acc.index:
            assert abs(r.pooled_gap - acc.loc[r.population, "gap (rule - k-NN)"]) < 1e-12, r.population
    kisti = whl.set_index("population").loc["kisti", "pooled_gap"]
    assert round(kisti, 6) == 0.113137, kisti
    print("the `all` rows reproduce phase2e_pooled_ads, _sv and _cells_sv to 1e-12 on the point gap; "
          "every frozen population reproduces phase2e_accuracy_by_population; kisti gap {:.6f}".format(kisti))
    print("verdicts of the `all` rows under the new p29b seeds that differ from the committed "
          "verdicts, over three margins: {}".format(flips))


def task_b(bk):
    t = order_bands(table(bk, ["init_band"], "p29b|all|init"), "init_band", INIT_BANDS)
    rows = [t.rename(columns={"init_band": "cell"}).assign(part="INIT band alone", dataset="all")]

    ref = pd.read_csv(TABLES / "phase2e_pooled_init_sv.csv")
    dec = ref[ref["verdict_0.05"].isin(DECIDED)]
    got = {(a, s): v for a, s, v in zip(dec.init_band, dec.sv_band, dec["verdict_0.05"])}
    if got != INIT_CELLS:
        sys.exit("HALT: phase2e_pooled_init_sv.csv decided cells at 0.05 are {} not {}".format(got, INIT_CELLS))
    for (ib, sb), want in INIT_CELLS.items():
        cell = bk[(bk.init_band == ib) & (bk.sv_band == sb)]
        label = "{} x {}".format(ib, sb)
        w = whole(cell, "p29b|{}|init_cell".format(label))
        r = ref[(ref.init_band == ib) & (ref.sv_band == sb)].iloc[0]
        assert abs(w.pooled_gap.iloc[0] - r.pooled_gap) < 1e-12 and w.n_test.iloc[0] == r.n_test, label
        rows.append(w.assign(part="cell", cell=label, dataset="all", committed_verdict_005=want))
        for d in sorted(cell.dataset.unique()):
            rows.append(whole(cell[cell.dataset == d], "p29b|{} in {}|init_cell".format(label, d))
                        .assign(part="cell, one dataset", cell=label, dataset=d))
            rows.append(whole(cell[cell.dataset != d], "p29b|{} without {}|init_cell".format(label, d))
                        .assign(part="cell, dataset left out", cell=label, dataset=d))
    out = pd.concat(rows, ignore_index=True)
    lead = ["part", "cell", "dataset"]
    return out[lead + [c for c in out.columns if c not in lead]]


def task_c():
    try:
        txt = subprocess.run(["git", "show", "v1.1.0:" + EXP1], cwd=HERE.parent, check=True,
                             capture_output=True, text=True).stdout
    except subprocess.CalledProcessError as e:
        sys.exit("HALT: cannot read {} from tag v1.1.0: {}".format(EXP1, e.stderr.strip()))
    e = pd.read_csv(io.StringIO(txt))
    assert len(e) == 240 and e.lexical_variation.dtype == bool, (len(e), e.lexical_variation.dtype)
    c = e[~e.lexical_variation].copy()
    assert len(c) == 120, len(c)
    c["inside_margin_0.02"] = ((c.paired_diff_ci_low >= -EXP1_MARGIN)
                               & (c.paired_diff_ci_high <= EXP1_MARGIN))
    cols = ["seed", "target_deterministic_share", "p_transform", "status", "paired_diff_point",
            "paired_diff_ci_low", "paired_diff_ci_high", "empirical_winner", "inside_margin_0.02"]
    return c[cols].sort_values(["target_deterministic_share", "seed"]).reset_index(drop=True)


def demo():
    """Assert-based self-check of `whole`, `table` and the leave-one-out on a toy block table."""
    c = PRIMARY
    toy = pd.DataFrame({"dataset": ["a", "a", "b", "b"], "ads_band": ["1.0", "1.0", "1.0", "[0,0.5)"],
                        "n_test": [4, 2, 3, 1], "net_" + c: [1, -1, 2, 0],
                        "rule_correct": [3, 1, 3, 1], "knn_correct_" + c: [2, 2, 1, 1],
                        "rule_fires_n": [4, 2, 3, 1], "agree_n_" + c: [2, 1, 1, 1],
                        PLUS: [1, 0, 2, 0], MINUS: [0, 1, 0, 0]})
    toy["gap_" + c] = toy["net_" + c] / toy.n_test
    for d in DELTAS:
        toy["bverdict_{}_{:.2f}".format(c, d)] = ["tie", "rule wins", "undecided", "k-NN wins"]
    w = whole(toy, "demo").iloc[0]
    assert abs(w.pooled_gap - 2 / 10) < 1e-12 and w.n_blocks == 4 and w.n_test == 10
    assert w.rule_right_vote_wrong == 3 and w.vote_right_rule_wrong == 1 and w.under_powered
    t = table(toy, ["ads_band"], "demo").set_index("ads_band")
    assert t.loc["1.0", "rule_right_vote_wrong"] == 3 and abs(t.loc["[0,0.5)", "pooled_gap"]) < 1e-12
    loo = whole(toy[toy.dataset != "a"], "demo").iloc[0]
    assert abs(loo.pooled_gap - 2 / 4) < 1e-12 and loo.n_blocks == 2
    assert w["n_decided_0.05"] == 2
    print("phase2_9b self-check: all assertions passed")


class Tee(io.StringIO):
    def __init__(self, out):
        super().__init__()
        self.out = out

    def write(self, s):
        self.out.write(s)
        return super().write(s)


def report(stdout, tabs):
    whl, bands, cells, struct, init, exp1 = tabs
    kept = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    hand = kept[kept.index(HAND):] if HAND in kept else HAND + "\n\nNot yet written.\n"
    st = struct[struct.outcome != "not eligible"]
    out = ["# Phase 2.9b step 1: per-population verdicts, the INIT control cells, and the "
           "Experiment 1 interval count", "",
           "Generated by `phase2/phase2_9b_supplement.py` from committed records, except the last "
           "section, which is hand-written. Intervals for sub-populations use new seeds "
           "(`p29b|<population>|<axis>`); the `all` rows are checked against the committed tables "
           "on the point gap. Under 30 blocks is under-powered and decides nothing.", "",
           "## Run output", "", "```", stdout.rstrip(), "```", "",
           "## Whole populations", "", md_table(whl, ["population"] + SHOW), "",
           "Table: reports/tables/phase2_9b_population_verdicts.csv", "",
           "## By ADS band and by SV band", "", md_table(bands, ["population", "axis", "band"] + SHOW), "",
           "Table: reports/tables/phase2_9b_bands_by_population.csv", "",
           "## The 5 by 4 grid, decided cells only", "",
           "Every cell of every population is in the table file; shown here are the cells "
           "decided at any margin, under-powered or not.", "",
           md_table(cells[cells[["verdict_{:.2f}".format(d) for d in DELTAS]].isin(DECIDED).any(axis=1)],
                    ["population", "ads_band", "sv_band"] + SHOW), "",
           "Table: reports/tables/phase2_9b_cells_by_population.csv", "",
           "## Winner structure", "",
           "Levels with fewer than two eligible bands are in the table file as `not eligible` "
           "and are left out here.", "",
           md_table(st, ["population", "direction", "delta", "fixed_level", "eligible_bands",
                         "decided_bands", "verdicts", "outcome"]), "",
           "Table: reports/tables/phase2_9b_structure_by_population.csv", "",
           "## The INIT control", "", md_table(init, ["part", "cell", "dataset"] + SHOW), "",
           "Table: reports/tables/phase2_9b_init.csv", "",
           "## Experiment 1, clean conditions, read from the `v1.1.0` tag", "",
           "{} of {} clean conditions have a paired-difference interval inside +-{}. Outside:".format(
               int(exp1["inside_margin_0.02"].sum()), len(exp1), EXP1_MARGIN), "",
           md_table(exp1[~exp1["inside_margin_0.02"]].astype({"seed": str})), "",
           "Table: reports/tables/phase2_9b_exp1_clean_intervals.csv", "",
           hand.rstrip(), ""]
    REPORT.write_text("\n".join(out), encoding="utf-8")


def main():
    tee = Tee(sys.stdout)
    with contextlib.redirect_stdout(tee):
        print("Python {}, {}".format(platform.python_version(), platform.platform()))
        for v in versions()[1:]:
            print(v)
        bk, _ = load()
        whl, bands, cells, struct = task_a(bk)
        check_against_committed(whl, bands, cells)
        init = task_b(bk)
        exp1 = task_c()
        tabs = (whl, bands, cells, struct, init, exp1)
        names = ("phase2_9b_population_verdicts.csv", "phase2_9b_bands_by_population.csv",
                 "phase2_9b_cells_by_population.csv", "phase2_9b_structure_by_population.csv",
                 "phase2_9b_init.csv", "phase2_9b_exp1_clean_intervals.csv")
        for df, name in zip(tabs, names):
            print("wrote", dump(df, name))
        out = exp1[~exp1["inside_margin_0.02"]]
        print("Experiment 1: {} of {} clean conditions inside +-{}; outside: {}".format(
            len(exp1) - len(out), len(exp1), EXP1_MARGIN,
            ", ".join("seed {} (share {})".format(s, t)
                      for s, t in zip(out.seed, out.target_deterministic_share))))
    report(tee.getvalue(), tabs)
    print("wrote reports/" + REPORT.name)


if __name__ == "__main__":
    demo()
    main()
