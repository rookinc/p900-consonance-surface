# P900 Phase 7 Candidate Binary Consonance Law

Status: candidate law sandbox

Warning: this is not a theorem and not a final P900 construction.

## Candidate law

For a G15 adjacency arising from two Petersen edges with shared Petersen vertex `v`:

- if `v` is even, use identity interface, shift 0 mod 60
- if `v` is odd, use half-turn interface, shift 30 mod 60

## Why this rule is preferred

Phase 6 compared tested binary 0/30 label families. This rule ranked best by no drift first, then identity/half-turn balance.

Phase 6 support:

- audited cycles: 557
- identity closures: 282
- half-turn closures: 275
- orientation drift: 0
- balance gap: 7

## Surface counts

- G15 positions: 15
- G15 edges: 30
- P900 states: 900
- edge label counts: {'half_turn': 15, 'identity': 15}
- external degree histogram: {4: 900}

## Interpretation

- This rule is incidence-derived rather than arbitrary index-derived.
- The rule uses Petersen shared-vertex parity to assign the inter-thalion interface.
- The rule preserves uniform external degree 4.
- The rule inherits Phase 6's best observed identity/half-turn cycle balance among tested binary label families.
- This is the current preferred baseline for P900 binary consonance.

## Edge law table

- G15 edge [0, 1] from Petersen edges [0, 1] and [1, 2]: shared vertex 1 (odd), half_turn shift 30 mod 60
- G15 edge [0, 4] from Petersen edges [0, 1] and [4, 0]: shared vertex 0 (even), identity shift 0 mod 60
- G15 edge [0, 5] from Petersen edges [0, 1] and [0, 5]: shared vertex 0 (even), identity shift 0 mod 60
- G15 edge [0, 6] from Petersen edges [0, 1] and [1, 6]: shared vertex 1 (odd), half_turn shift 30 mod 60
- G15 edge [1, 2] from Petersen edges [1, 2] and [2, 3]: shared vertex 2 (even), identity shift 0 mod 60
- G15 edge [1, 6] from Petersen edges [1, 2] and [1, 6]: shared vertex 1 (odd), half_turn shift 30 mod 60
- G15 edge [1, 7] from Petersen edges [1, 2] and [2, 7]: shared vertex 2 (even), identity shift 0 mod 60
- G15 edge [2, 3] from Petersen edges [2, 3] and [3, 4]: shared vertex 3 (odd), half_turn shift 30 mod 60
- G15 edge [2, 7] from Petersen edges [2, 3] and [2, 7]: shared vertex 2 (even), identity shift 0 mod 60
- G15 edge [2, 8] from Petersen edges [2, 3] and [3, 8]: shared vertex 3 (odd), half_turn shift 30 mod 60
- G15 edge [3, 4] from Petersen edges [3, 4] and [4, 0]: shared vertex 4 (even), identity shift 0 mod 60
- G15 edge [3, 8] from Petersen edges [3, 4] and [3, 8]: shared vertex 3 (odd), half_turn shift 30 mod 60
- G15 edge [3, 9] from Petersen edges [3, 4] and [4, 9]: shared vertex 4 (even), identity shift 0 mod 60
- G15 edge [4, 5] from Petersen edges [4, 0] and [0, 5]: shared vertex 0 (even), identity shift 0 mod 60
- G15 edge [4, 9] from Petersen edges [4, 0] and [4, 9]: shared vertex 4 (even), identity shift 0 mod 60
- G15 edge [5, 10] from Petersen edges [0, 5] and [5, 7]: shared vertex 5 (odd), half_turn shift 30 mod 60
- G15 edge [5, 14] from Petersen edges [0, 5] and [8, 5]: shared vertex 5 (odd), half_turn shift 30 mod 60
- G15 edge [6, 12] from Petersen edges [1, 6] and [9, 6]: shared vertex 6 (even), identity shift 0 mod 60
- G15 edge [6, 13] from Petersen edges [1, 6] and [6, 8]: shared vertex 6 (even), identity shift 0 mod 60
- G15 edge [7, 10] from Petersen edges [2, 7] and [5, 7]: shared vertex 7 (odd), half_turn shift 30 mod 60
- G15 edge [7, 11] from Petersen edges [2, 7] and [7, 9]: shared vertex 7 (odd), half_turn shift 30 mod 60
- G15 edge [8, 13] from Petersen edges [3, 8] and [6, 8]: shared vertex 8 (even), identity shift 0 mod 60
- G15 edge [8, 14] from Petersen edges [3, 8] and [8, 5]: shared vertex 8 (even), identity shift 0 mod 60
- G15 edge [9, 11] from Petersen edges [4, 9] and [7, 9]: shared vertex 9 (odd), half_turn shift 30 mod 60
- G15 edge [9, 12] from Petersen edges [4, 9] and [9, 6]: shared vertex 9 (odd), half_turn shift 30 mod 60
- G15 edge [10, 11] from Petersen edges [5, 7] and [7, 9]: shared vertex 7 (odd), half_turn shift 30 mod 60
- G15 edge [10, 14] from Petersen edges [5, 7] and [8, 5]: shared vertex 5 (odd), half_turn shift 30 mod 60
- G15 edge [11, 12] from Petersen edges [7, 9] and [9, 6]: shared vertex 9 (odd), half_turn shift 30 mod 60
- G15 edge [12, 13] from Petersen edges [9, 6] and [6, 8]: shared vertex 6 (even), identity shift 0 mod 60
- G15 edge [13, 14] from Petersen edges [6, 8] and [8, 5]: shared vertex 8 (even), identity shift 0 mod 60
