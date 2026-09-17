"""FROZEN Phase 2.1 definitions: what a name block is, and what a surface form is.

Charter invariant 5 says freeze these before measuring anything. They are frozen
here, in one committed file, before any accuracy, mechanism, cutoff or selector
exists. Nothing downstream may re-tune them.

Three definitions live here.

1. `block_key(first, last)` - the blocking normalization. Rule, in full:

       first initial + " " + last name, after transliterating to ASCII,
       lowercasing, and deleting every character that is not an ASCII letter.

   S2AND ships its own `author_info.block` field with the same intent ("first
   initial + last name", `s2and/text.py::compute_block`), and we report every
   measurement against that field too, as a robustness check. We do not use it
   as the key of record for two reasons, both measured, not assumed:

   - It is not a function of the name. The same (first, middle, last) triple
     maps to two different shipped blocks for 0.76% of inspire signatures
     (for example 'Murray Gell-Mann' appears under both 'm gell-mann' and
     'm gellmann'), because hyphens were handled two ways in preprocessing.
   - It keeps internal spaces and hyphens, so 'Gell-Mann' and 'Gellmann', or
     'De Simone' and 'DeSimone', land in different blocks. Deleting non-letters
     is the ordinary surname-plus-initial blocking of the AND literature and is
     the stricter, single-valued choice.

   Coarsening a key raises measured ambiguity, so this choice could in principle
   buy ADS range. It is frozen before any measurement, and the ADS distribution
   is reported under both this key and the shipped S2AND block so a reader can
   see the answer does not depend on it.

2. `surface_form(...)` - the surface string a mechanism would actually match on.
   The signature's own name parts, joined by single spaces, whitespace collapsed.
   Case, punctuation and diacritics are kept, because they *are* the surface
   variation we are trying to measure. Verified byte-identical to the raw
   `author_name` printed on the paper (see `ingest_s2and.py`'s roundtrip check).

3. `surface_variability(...)` - the per-block surface axis. The expected
   normalized Levenshtein distance between two signatures drawn at random
   without replacement from the block. Signature-weighted, so a block of 100
   identical strings plus one variant scores near 0, which is what "exact match
   would survive here" means. Undefined (None) for single-signature blocks.

`s2and_full_name` and `s2and_normalize_text` reproduce S2AND's own name
normalization (`s2and/text.py::normalize_text`,
`s2and/data.py::get_full_name_for_features`) and exist only so that S2AND's
published homonymity and synonymity measures can be recomputed on their own
terms for the cross-check.

Run `python phase2/s2and_blocking.py` for the self-check.
"""

import re
from collections.abc import Mapping

from rapidfuzz.distance import Levenshtein
from unidecode import unidecode

NON_LETTER = re.compile(r"[^a-z]+")
WHITESPACE = re.compile(r"\s+")
# S2AND's own rule, verbatim from s2and/text.py.
S2AND_RE_NORMALIZE_WHOLE_NAME = re.compile(r"[^a-zA-Z\s]+")


def _letters(text):
    """Transliterate to ASCII, lowercase, keep only a-z."""
    return NON_LETTER.sub("", unidecode(text or "").lower())


def block_key(first, last):
    """The frozen name block key: first initial + normalized last name.

    Returns "" when the last name has no ASCII letters at all; the caller drops
    those signatures and reports the count.
    """
    last_norm = _letters(last)
    if not last_norm:
        return ""
    return f"{_letters(first)[:1]} {last_norm}".strip()


def surface_form(first, middle, last, suffix):
    """The frozen surface string: the name parts as written, whitespace collapsed."""
    parts = [p.strip() for p in (first, middle, last, suffix) if p and p.strip()]
    return WHITESPACE.sub(" ", " ".join(parts)).strip()


def surface_variability(form_counts: Mapping[str, int]):
    """Expected normalized edit distance between two signatures of one block.

    `form_counts` maps each distinct surface form to how many signatures carry
    it. Identical-form pairs contribute distance 0, so only distinct-form pairs
    need computing: O(k^2) in distinct forms, not O(n^2) in signatures.
    """
    n = sum(form_counts.values())
    if n < 2:
        return None
    forms = list(form_counts)
    total = 0.0
    for i, a in enumerate(forms):
        ca = form_counts[a]
        for b in forms[i + 1:]:
            total += ca * form_counts[b] * Levenshtein.normalized_distance(a, b)
    return total / (n * (n - 1) / 2)


def s2and_normalize_text(text, special_case_apostrophes=False):
    """S2AND's `normalize_text`, reproduced for the cross-check only."""
    if not text:
        return ""
    norm = unidecode(text).lower()
    if special_case_apostrophes:
        norm = norm.replace("'", "")
    norm = S2AND_RE_NORMALIZE_WHOLE_NAME.sub(" ", norm)
    return WHITESPACE.sub(" ", norm).strip()


def s2and_full_name(first, middle, last, suffix):
    """S2AND's `get_full_name_for_features`, reproduced for the cross-check only.

    S2AND's homonymity and synonymity compare signatures on *this* string, not
    on the raw surface form, so the cross-check has to use it.
    """
    parts = [
        s2and_normalize_text(first, special_case_apostrophes=True),
        s2and_normalize_text(middle, special_case_apostrophes=True),
        s2and_normalize_text(last),
        s2and_normalize_text(suffix),
    ]
    return " ".join(p for p in parts if p)


def demo():
    """Self-check. Fails loudly if any frozen definition drifts."""
    assert block_key("Murray", "Gell-Mann") == "m gellmann"
    assert block_key("M.", "Gellmann") == "m gellmann", "hyphen and initial forms must collide"
    assert block_key("Andrea", "De Simone") == "a desimone"
    assert block_key("Abo-el-nour", "Abd-alla") == "a abdalla"
    assert block_key(None, "Su") == "su", "no first name -> bare last name"
    assert block_key("Jane", "") == "", "unusable last name -> empty key"
    assert block_key("Jane", "张") == "j zhang", "CJK last names transliterate, they are not dropped"
    assert block_key("Jane", "123") == "", "last name with no letters -> empty key"

    assert surface_form("Abo-el-nour", "N.", "Abd-alla", None) == "Abo-el-nour N. Abd-alla"
    assert surface_form("  Jane ", None, "Smith", "Jr.") == "Jane Smith Jr."
    assert surface_form("Jürgen", None, "Müller", None) == "Jürgen Müller", "diacritics kept"

    assert surface_variability({"jane smith": 1}) is None
    assert surface_variability({"jane smith": 5}) == 0.0, "all identical -> zero variability"
    # two signatures, one char apart out of 10 -> 0.1
    assert abs(surface_variability({"jane smith": 1, "jane smitn": 1}) - 0.1) < 1e-12
    # 3 of the same + 1 variant -> only 3 of the 6 pairs are non-identical
    v = surface_variability({"jane smith": 3, "jane smitn": 1})
    assert abs(v - (3 * 0.1) / 6) < 1e-12, v
    # weighting must matter: same two forms, different multiplicities
    assert surface_variability({"a": 1, "bbbb": 1}) > surface_variability({"a": 99, "bbbb": 1})

    assert s2and_full_name("Abo-el-nour", "N.", "Abd-alla", None) == "abo el nour n abd alla"
    assert s2and_full_name("Jürgen", None, "Müller", None) == "jurgen muller"
    assert s2and_normalize_text("O'Brien", special_case_apostrophes=True) == "obrien"

    print("s2and_blocking self-check: all assertions passed")


if __name__ == "__main__":
    demo()
