# P900 Phase 26 Preference Tension Checkpoint

Status: preference_tension_recorded

Warning: This records a selector tension. It does not choose a final P900 law.

## Pre-G60 selector

- selector: local cycle-length balance score
- preferred: {'family': 'gap1_orbit_2_representative', 'half_turn_set': [0, 1, 2, 3, 9], 'local_balance_score': 13, 'max_length_gap': 7, 'per_length_scores': {'3': {'half_turn_closure': 5, 'identity_closure': 5, 'length_balance_gap': 0, 'orientation_drift': 0}, '5': {'half_turn_closure': 6, 'identity_closure': 6, 'length_balance_gap': 0, 'orientation_drift': 0}, '6': {'half_turn_closure': 32, 'identity_closure': 38, 'length_balance_gap': 6, 'orientation_drift': 0}, '7': {'half_turn_closure': 90, 'identity_closure': 90, 'length_balance_gap': 0, 'orientation_drift': 0}, '8': {'half_turn_closure': 146, 'identity_closure': 139, 'length_balance_gap': 7, 'orientation_drift': 0}}, 'perfectly_balanced_length_count': 3, 'total_balance_gap': 1, 'total_half_turn_closures': 279, 'total_identity_closures': 278, 'total_orientation_drift': 0}
- interpretation: Orbit 2 was preferred before G60 import because it had the lower local balance score.

## Post-G60 selector

- selector: basic global tightness after internal G60 overlay
- preferred_by_fewer_diameter8_vertices: gap1_orbit_1_representative
- orbit1_eccentricity_histogram: {'6': 342, '7': 526, '8': 32}
- orbit2_eccentricity_histogram: {'6': 327, '7': 525, '8': 48}
- orbit1_diameter8_vertices: 32
- orbit2_diameter8_vertices: 48
- orbit1_eccentricity6_vertices: 342
- orbit2_eccentricity6_vertices: 327
- interpretation: Orbit 1 is globally tighter by this crude distance criterion because it has fewer diameter-8 vertices and more eccentricity-6 vertices.

## Common closure facts

- both_connected: True
- same_degree_histogram: True
- same_combined_edge_count: True
- same_diameter: True
- diameter: 8
- degree_histogram: {'8': 900}
- combined_edge_count: 3600

## Working position

- The gap-1 orbit family, not a single labeled representative, is the current closure-bearing object.
- The Phase 15 preference for Orbit 2 remains meaningful as a pre-G60 local-balance result.
- The Phase 25 post-G60 global-distance result favors Orbit 1 under a different criterion.
- Because the selectors disagree, the project should not declare either orbit final.
- The next selector must combine local balance, closure, distance-shell behavior, and layer recoverability.

## Safe language

- preference tension
- multi-invariant selector
- closure-bearing gap-1 family
- Orbit 2 local-balance preference
- Orbit 1 global-tightness preference

## Avoid language

- Orbit 1 is the final law
- Orbit 2 is the final law
- Phase 25 overturns Phase 15
- Phase 15 proves Orbit 2 canonical
- closure alone selects the preferred orbit

## Next tests

- Build a multi-invariant selector table for both gap-1 orbit representatives.
- Add all-root shell profile histograms, not only sampled roots.
- Audit layer recoverability: can G15 sectors, G60 copies, and G30 sheet residues be recovered after overlay?
- Compare automorphism or relabeling stability of the combined graphs.
- Export both combined candidates for renderer inspection.
