# P900 Phase 27 Multi-Invariant Selector

Status: multi_invariant_selector_checkpoint

Warning: This is a selector checkpoint, not a final P900 law or uniqueness proof.

## Selector table

### gap1_orbit_1_representative

- half_turn_set: [0, 1, 2, 3, 5]
- identity_set: [4, 6, 7, 8, 9]
- closes_after_g60: True
- degree_histogram: {'8': 900}
- combined_edge_count: 3600
- diameter: 8
- local_balance_score: 17
- max_length_gap: 8
- perfectly_balanced_length_count: 2
- total_balance_gap: 1
- eccentricity_histogram: {'6': 342, '7': 526, '8': 32}
- diameter8_vertices: 32
- eccentricity6_vertices: 342

### gap1_orbit_2_representative

- half_turn_set: [0, 1, 2, 3, 9]
- identity_set: [4, 5, 6, 7, 8]
- closes_after_g60: True
- degree_histogram: {'8': 900}
- combined_edge_count: 3600
- diameter: 8
- local_balance_score: 13
- max_length_gap: 7
- perfectly_balanced_length_count: 3
- total_balance_gap: 1
- eccentricity_histogram: {'6': 327, '7': 525, '8': 48}
- diameter8_vertices: 48
- eccentricity6_vertices: 327

## Criteria winners

- local_balance_score: ['gap1_orbit_2_representative'] at 13
- max_length_gap: ['gap1_orbit_2_representative'] at 7
- perfectly_balanced_length_count: ['gap1_orbit_2_representative'] at 3
- diameter8_vertices: ['gap1_orbit_1_representative'] at 32
- eccentricity6_vertices: ['gap1_orbit_1_representative'] at 342

## Scorecard

- gap1_orbit_1_representative: 2.0
- gap1_orbit_2_representative: 3.0

## Provisional selector

gap1_orbit_2_representative

## Interpretation

- Both gap-1 orbit representatives remain closure-bearing after internal G60 import.
- Orbit 2 remains favored by pre-G60 local cycle-balance measures.
- Orbit 1 is favored by post-G60 global tightness measures.
- The multi-invariant selector records this tension rather than erasing it.
- A final selector should wait for layer recoverability, all-root shells, and automorphism/relabeling tests.

## Safe language

- multi-invariant selector checkpoint
- provisional selector
- closure-bearing candidates
- local-balance criterion
- global-tightness criterion

## Avoid language

- final P900 law
- unique P900 graph
- canonical representative selected
- Orbit 1 defeats Orbit 2
- Orbit 2 defeats Orbit 1

## Next tests

- Phase 28 all-root shell profile comparison.
- Phase 29 layer recoverability audit.
- Phase 30 combined graph export for Aletheos renderer.
