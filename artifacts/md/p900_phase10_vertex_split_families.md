# P900 Phase 10 Vertex Split Family Audit

Status: sandbox audit

Warning: this compares 5-and-5 Petersen vertex splits as binary half-turn sets. It does not prove a final P900 law.

## Purpose

Phase 10 asks whether the candidate odd-vertex half-turn set is special among all 5-of-10 Petersen vertex splits.

## Counts

- cycles audited: 557
- tested half-turn sets: 252
- best balance gap: 1
- best profile count: 120
- candidate half-turn set: [1, 3, 5, 7, 9]
- candidate rank: 165
- candidate profile: {'half_turn_set': [1, 3, 5, 7, 9], 'edge_label_counts': {'half_turn': 15, 'identity': 15}, 'identity_closure_count': 282, 'half_turn_closure_count': 275, 'orientation_drift_count': 0, 'identity_half_turn_balance_gap': 7, 'holonomy_shift_histogram_mod_60': {0: 282, 30: 275}, 'closure_type_histogram': {'half_turn_closure': 275, 'identity_closure': 282}}

## Gap histogram

- gap 1: 120
- gap 7: 60
- gap 15: 12
- gap 17: 60

## Top profiles

- rank 1: set [0, 1, 2, 3, 5], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 2: set [0, 1, 2, 3, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 3: set [0, 1, 2, 3, 9], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 4: set [0, 1, 2, 4, 7], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 5: set [0, 1, 2, 4, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 6: set [0, 1, 2, 4, 9], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 7: set [0, 1, 2, 5, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 8: set [0, 1, 2, 5, 9], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 9: set [0, 1, 2, 7, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 10: set [0, 1, 2, 7, 9], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 11: set [0, 1, 3, 4, 6], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 12: set [0, 1, 3, 4, 7], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 13: set [0, 1, 3, 4, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 14: set [0, 1, 3, 5, 6], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 15: set [0, 1, 3, 5, 7], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 16: set [0, 1, 3, 5, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 17: set [0, 1, 3, 6, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 18: set [0, 1, 3, 6, 9], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 19: set [0, 1, 4, 6, 7], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}
- rank 20: set [0, 1, 4, 6, 8], identity 278, half-turn 279, drift 0, gap 1, edge labels {'half_turn': 15, 'identity': 15}

## First read

- Phase 10 tests whether the candidate odd-vertex half-turn set is special among all 5-of-10 Petersen vertex splits.
- Every 5-set is used as a half-turn set; its complement is identity.
- The discriminator is the identity/half-turn closure balance over audited G15 cycles.
- A low rank means the candidate split is not merely arbitrary.
