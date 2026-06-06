# P900 Phase 30 Combined Graph Export

Status: renderer_export_ok

Warning: This is a renderer/export artifact. It does not select a final P900 law.

## Export purpose

Export both closure-bearing combined P900 candidates for Aletheos renderer integration.

## Renderer defaults

- default_candidate: gap1_orbit_2_representative
- default_view: combined
- available_views: ['combined', 'internal_g60', 'external_p900', 'residue_sheets', 'sector_fibers']

## Candidates

### gap1_orbit_1_representative

- id: gap1_orbit_1
- role: global-tightness candidate
- half_turn_set: [0, 1, 2, 3, 5]
- identity_set: [4, 6, 7, 8, 9]
- vertices: 900
- internal_edges: 1800
- external_edges: 1800
- combined_edges: 3600
- duplicate_edges: 0
- degree_histogram: {8: 900}
- edge_class_counts: {'external_half_turn_mod30': 900, 'external_identity_same_local': 900, 'internal_same_sector': 1800}

### gap1_orbit_2_representative

- id: gap1_orbit_2
- role: local-balance provisional selector
- half_turn_set: [0, 1, 2, 3, 9]
- identity_set: [4, 5, 6, 7, 8]
- vertices: 900
- internal_edges: 1800
- external_edges: 1800
- combined_edges: 3600
- duplicate_edges: 0
- degree_histogram: {8: 900}
- edge_class_counts: {'external_half_turn_mod30': 900, 'external_identity_same_local': 900, 'internal_same_sector': 1800}

## Checks

- vertex_count_is_900: True
- candidate_count_is_2: True
- all_candidates_have_1800_internal_edges: True
- all_candidates_have_1800_external_edges: True
- all_candidates_have_3600_combined_edges: True
- all_candidates_have_no_duplicate_edges: True
- all_candidates_are_8_regular: True
- phase29_layer_recoverability_ok_for_both: True

## First read

- Phase 30 exports both closure-bearing P900 candidates.
- Orbit 2 remains the provisional selector from Phase 27.
- Orbit 1 remains the global-tightness candidate.
- Each export preserves internal, external, and combined edge classes for renderer toggles.
- The renderer can now show body, surface, and body-plus-surface views without recomputing graph structure.
