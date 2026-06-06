# P900 Phase 8 Candidate Law Verification Packet

Status: verified_sandbox_checkpoint

Warning: this verifies an internal sandbox checkpoint, not a theorem and not a final P900 construction.

## Candidate law

Name: `shared_vertex_parity_binary_consonance`

Rule:

- shared Petersen vertex even: identity interface, shift 0 mod 60
- shared Petersen vertex odd: half-turn interface, shift 30 mod 60

## Verification checks

- p900_state_count_is_900: True
- candidate_edge_labels_balanced_15_15: True
- candidate_external_degree_uniform_4: True
- phase4_arbitrary_stitching_detected_drift: True
- phase5_binary_half_turn_removed_drift: True
- phase6_candidate_ranked_first: True
- phase6_candidate_balance_gap_7: True
- phase7_candidate_law_named: True

verification_ok: True

## Phase summary

### phase1

- claim: same-index G15 coupling gives uniform external degree
- external_degree_histogram: {'4': 900}
- coupling_edges: 1800

### phase2

- claim: simple global orientation maps preserve uniform external degree
- all_variants_uniform_external_degree_4: True
- tested_maps: ['identity', 'half_turn_plus_30', 'forward_step_plus_1', 'backward_step_minus_1']

### phase3

- claim: heterogeneous edge-labeled stitching preserves uniform external degree
- uniform_external_degree_4: True
- edge_label_counts: {'backward_step_minus_1': 7, 'forward_step_plus_1': 7, 'half_turn_plus_30': 8, 'identity': 8}

### phase4

- claim: arbitrary stitched shifts produce orientation drift
- closure_type_histogram: {'half_turn_closure': 72, 'identity_closure': 67, 'orientation_drift': 418}

### phase5

- claim: binary 0/30 sign grammar eliminates orientation drift
- closure_type_histogram: {'half_turn_closure': 269, 'identity_closure': 288}
- holonomy_shift_histogram_mod_60: {'0': 288, '30': 269}

### phase6

- claim: shared-vertex parity is best among tested binary label families
- ranked_by_no_drift_then_balance: ['shared_vertex_odd_half_turn', 'inner_touch_half_turn', 'outer_touch_half_turn', 'alternating_index', 'all_half_turn', 'all_identity', 'different_petersen_edge_type_half_turn', 'spoke_touch_half_turn']
- winner: shared_vertex_odd_half_turn
- winner_summary: {'closure_type_histogram': {'half_turn_closure': 275, 'identity_closure': 282}, 'edge_label_counts': {'half_turn': 15, 'identity': 15}, 'half_turn_closure_count': 275, 'holonomy_shift_histogram_mod_60': {'0': 282, '30': 275}, 'identity_closure_count': 282, 'identity_half_turn_balance_gap': 7, 'length_closure_histogram': {'3': {'half_turn_closure': 5, 'identity_closure': 5}, '5': {'half_turn_closure': 6, 'identity_closure': 6}, '6': {'half_turn_closure': 30, 'identity_closure': 40}, '7': {'half_turn_closure': 90, 'identity_closure': 90}, '8': {'half_turn_closure': 144, 'identity_closure': 141}}, 'orientation_drift_count': 0}

### phase7

- claim: candidate law promoted as shared_vertex_parity_binary_consonance
- edge_label_counts: {'half_turn': 15, 'identity': 15}
- external_degree_histogram: {'4': 900}
- phase6_support: {'cycle_count_audited': 557, 'half_turn_closure_count': 275, 'identity_closure_count': 282, 'identity_half_turn_balance_gap': 7, 'orientation_drift_count': 0, 'ranking': 'best among tested binary label families by no drift then identity/half-turn balance'}

## Working interpretation

- P900 is currently treated as a candidate consonance surface, not a proven graph identity.
- The surface address space is 15 x 60 = 900.
- G15 = L(Petersen) supplies the inter-thalion adjacency grammar.
- Arbitrary local shifts preserve degree but cause cycle holonomy drift.
- Binary 0/30 shifts preserve degree and restrict cycle holonomy to identity or half-turn.
- The best tested binary incidence-derived rule assigns identity or half-turn by parity of the shared Petersen vertex.

## Next steps

- add a compact README checkpoint section
- add internal G60 data when canonical source files are available
- compare the candidate binary law against M-guided and Q-guided interfaces
- audit whether candidate law is invariant under relabelings or depends on chosen Petersen labeling
