"""FROZEN Phase 2.2b calibration constants.

Produced once by `phase2b_build.py` on the calibration split only, which is
disjoint at block level from every block that produces a reported number.
Committed before any evaluation-split run, per PREREG sections 6 and 7.
Do not edit. Re-running `phase2b_build.py` reproduces this file exactly.
"""

SEED = 20260918
N_CALIBRATION_BLOCKS = 2848
N_LIVE_BLOCKS = 18984

# PREREG section 7: one global cutoff per metric family, highest pooled
# calibration accuracy, ties broken toward the higher cutoff.
FUZZY_CUTOFF = {
    'levenshtein': 0.50,
    'jarowinkler': 0.50,
}

# PREREG section 6: terciles of the strictly positive values, calibration split.
SV_BAND_EDGES = (0.102644366116, 0.195066351488)
SV_RESID_BAND_EDGES = (0.036781609195, 0.082417582418)

# The full accuracy-versus-cutoff curve PREREG section 7 step 5 requires,
# as (cutoff, pooled fuzzy accuracy, fuzzy coverage) on the calibration split.
CUTOFF_CURVE = {
    'levenshtein': [
        (0.50, 0.844091, 0.998671),
        (0.55, 0.843427, 0.997398),
        (0.60, 0.842458, 0.996070),
        (0.65, 0.840686, 0.993385),
        (0.70, 0.839358, 0.990811),
        (0.75, 0.837753, 0.987794),
        (0.80, 0.835538, 0.983808),
        (0.85, 0.831774, 0.978494),
        (0.90, 0.829089, 0.974481),
        (0.95, 0.822751, 0.966538),
    ],
    'jarowinkler': [
        (0.50, 0.844368, 0.999889),
        (0.55, 0.844229, 0.999696),
        (0.60, 0.844035, 0.999308),
        (0.65, 0.843952, 0.998810),
        (0.70, 0.843122, 0.997703),
        (0.75, 0.842485, 0.996845),
        (0.80, 0.840797, 0.994409),
        (0.85, 0.839413, 0.991531),
        (0.90, 0.837337, 0.986936),
        (0.95, 0.832272, 0.978577),
    ],
}
