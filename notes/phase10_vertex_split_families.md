# Phase 10 Vertex Split Family Audit

Status: sandbox audit

Phase 10 asks whether the candidate odd-vertex half-turn set is special among all 5-of-10 Petersen vertex splits.

Candidate from Phase 7:

    half-turn set = {1, 3, 5, 7, 9}
    identity set  = {0, 2, 4, 6, 8}

Audit:

    test all 252 subsets of 5 Petersen vertices as the half-turn set
    compute identity/half-turn closure balance over G15 cycles
    rank by orientation drift first, then balance gap

Interpretation:

    if the candidate ranks highly, it is not merely arbitrary
    if many splits tie it, the rule is part of a broader family
