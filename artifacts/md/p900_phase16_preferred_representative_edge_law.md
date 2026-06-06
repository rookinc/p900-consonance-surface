# P900 Phase 16 Preferred Representative Edge Law

Status: preferred representative checkpoint

Warning: this is a preferred representative for the next tests, not a final P900 law.

## Preferred representative

- family: gap1_orbit_2_representative
- half-turn set: [0, 1, 2, 3, 9]
- identity set: [4, 5, 6, 7, 8]

## Rule

For a G15 adjacency arising from two Petersen edges with shared Petersen vertex `v`:

- if `v` is in `[0, 1, 2, 3, 9]`, use half-turn interface, shift 30 mod 60
- otherwise, use identity interface, shift 0 mod 60

## Support

- total_identity_closures: 278
- total_half_turn_closures: 279
- orientation_drift: 0
- total_balance_gap: 1
- local_balance_score: 13
- max_length_gap: 7
- perfectly_balanced_length_count: 3

## Surface counts

- g15_positions: 15
- p900_states: 900
- external_degree: 4
- inter_thalion_edges: 1800
- edge label counts: {'half_turn': 15, 'identity': 15}

## Edge law table

- G15 edge [0, 1] from Petersen edges [0, 1] and [1, 2]: shared vertex 1, half_turn shift 30 mod 60
- G15 edge [0, 4] from Petersen edges [0, 1] and [4, 0]: shared vertex 0, half_turn shift 30 mod 60
- G15 edge [0, 5] from Petersen edges [0, 1] and [0, 5]: shared vertex 0, half_turn shift 30 mod 60
- G15 edge [0, 6] from Petersen edges [0, 1] and [1, 6]: shared vertex 1, half_turn shift 30 mod 60
- G15 edge [1, 2] from Petersen edges [1, 2] and [2, 3]: shared vertex 2, half_turn shift 30 mod 60
- G15 edge [1, 6] from Petersen edges [1, 2] and [1, 6]: shared vertex 1, half_turn shift 30 mod 60
- G15 edge [1, 7] from Petersen edges [1, 2] and [2, 7]: shared vertex 2, half_turn shift 30 mod 60
- G15 edge [2, 3] from Petersen edges [2, 3] and [3, 4]: shared vertex 3, half_turn shift 30 mod 60
- G15 edge [2, 7] from Petersen edges [2, 3] and [2, 7]: shared vertex 2, half_turn shift 30 mod 60
- G15 edge [2, 8] from Petersen edges [2, 3] and [3, 8]: shared vertex 3, half_turn shift 30 mod 60
- G15 edge [3, 4] from Petersen edges [3, 4] and [4, 0]: shared vertex 4, identity shift 0 mod 60
- G15 edge [3, 8] from Petersen edges [3, 4] and [3, 8]: shared vertex 3, half_turn shift 30 mod 60
- G15 edge [3, 9] from Petersen edges [3, 4] and [4, 9]: shared vertex 4, identity shift 0 mod 60
- G15 edge [4, 5] from Petersen edges [4, 0] and [0, 5]: shared vertex 0, half_turn shift 30 mod 60
- G15 edge [4, 9] from Petersen edges [4, 0] and [4, 9]: shared vertex 4, identity shift 0 mod 60
- G15 edge [5, 10] from Petersen edges [0, 5] and [5, 7]: shared vertex 5, identity shift 0 mod 60
- G15 edge [5, 14] from Petersen edges [0, 5] and [8, 5]: shared vertex 5, identity shift 0 mod 60
- G15 edge [6, 12] from Petersen edges [1, 6] and [9, 6]: shared vertex 6, identity shift 0 mod 60
- G15 edge [6, 13] from Petersen edges [1, 6] and [6, 8]: shared vertex 6, identity shift 0 mod 60
- G15 edge [7, 10] from Petersen edges [2, 7] and [5, 7]: shared vertex 7, identity shift 0 mod 60
- G15 edge [7, 11] from Petersen edges [2, 7] and [7, 9]: shared vertex 7, identity shift 0 mod 60
- G15 edge [8, 13] from Petersen edges [3, 8] and [6, 8]: shared vertex 8, identity shift 0 mod 60
- G15 edge [8, 14] from Petersen edges [3, 8] and [8, 5]: shared vertex 8, identity shift 0 mod 60
- G15 edge [9, 11] from Petersen edges [4, 9] and [7, 9]: shared vertex 9, half_turn shift 30 mod 60
- G15 edge [9, 12] from Petersen edges [4, 9] and [9, 6]: shared vertex 9, half_turn shift 30 mod 60
- G15 edge [10, 11] from Petersen edges [5, 7] and [7, 9]: shared vertex 7, identity shift 0 mod 60
- G15 edge [10, 14] from Petersen edges [5, 7] and [8, 5]: shared vertex 5, identity shift 0 mod 60
- G15 edge [11, 12] from Petersen edges [7, 9] and [9, 6]: shared vertex 9, half_turn shift 30 mod 60
- G15 edge [12, 13] from Petersen edges [9, 6] and [6, 8]: shared vertex 6, identity shift 0 mod 60
- G15 edge [13, 14] from Petersen edges [6, 8] and [8, 5]: shared vertex 8, identity shift 0 mod 60

## Working position

- This representative is selected from one of the two best gap-1 Petersen split orbits.
- It is preferred over the other tested representative by local balance score.
- Both gap-1 orbit families remain alive.
- This edge-law table gives a concrete interface rule for subsequent P900 tests.

## Next tests

- build explicit P900 external edge list for this representative
- audit connectedness and degree distribution of the external-only surface
- add a companion edge-law table for the other gap-1 family if needed
- prepare for internal G60 edge import
