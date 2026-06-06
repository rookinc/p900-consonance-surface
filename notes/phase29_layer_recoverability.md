# P900 Phase 29 Layer Recoverability Audit

Status: layer_recoverability_ok_for_both_gap1_orbits

Warning: This audits recoverability of known address layers. It does not prove canonical uniqueness.

## Purpose

Test whether G15 sector fibers, internal G60 copies, and G30 residue sheets remain recoverable after overlay.

## Comparison

- both_layer_recoverability_ok: True
- same_edge_class_counts: True
- same_sector_internal_histogram: True
- same_residue_external_histogram: True
- same_sector_pair_external_histogram: True

## Candidate audits

### gap1_orbit_1_representative

- half_turn_set: [0, 1, 2, 3, 5]
- identity_set: [4, 6, 7, 8, 9]
- combined_edge_count: 3600
- edge_class_counts: {'external_half_turn_mod30': 900, 'external_identity_same_local': 900, 'internal_same_sector': 1800}
- sector_internal_edge_count_histogram: {120: 15}
- residue_external_edge_count_histogram: {60: 30}
- sector_pair_external_edge_count_histogram: {60: 30}

Checks:

- combined_edge_count_is_3600: True
- internal_edges_are_same_sector: True
- external_edges_are_shift_0_or_30: True
- unexpected_edge_count_is_0: True
- all_sector_fibers_have_60_vertices: True
- all_sector_fibers_have_120_internal_edges: True
- all_residue_sheets_have_30_vertices: True
- all_residue_sheets_have_60_external_edges: True
- all_g15_sector_pairs_have_60_external_edges: True
- layer_recoverability_ok: True

### gap1_orbit_2_representative

- half_turn_set: [0, 1, 2, 3, 9]
- identity_set: [4, 5, 6, 7, 8]
- combined_edge_count: 3600
- edge_class_counts: {'external_half_turn_mod30': 900, 'external_identity_same_local': 900, 'internal_same_sector': 1800}
- sector_internal_edge_count_histogram: {120: 15}
- residue_external_edge_count_histogram: {60: 30}
- sector_pair_external_edge_count_histogram: {60: 30}

Checks:

- combined_edge_count_is_3600: True
- internal_edges_are_same_sector: True
- external_edges_are_shift_0_or_30: True
- unexpected_edge_count_is_0: True
- all_sector_fibers_have_60_vertices: True
- all_sector_fibers_have_120_internal_edges: True
- all_residue_sheets_have_30_vertices: True
- all_residue_sheets_have_60_external_edges: True
- all_g15_sector_pairs_have_60_external_edges: True
- layer_recoverability_ok: True

## First read

- Phase 29 checks whether the combined P900 graph still preserves the address-layer grammar.
- Internal G60 edges should be exactly the same-sector edges.
- External P900 edges should be exactly the inter-sector shift-0 or shift-30 edges.
- Each sector fiber should recover one 60-state G60 copy with 120 internal edges.
- Each mod-30 residue sheet should recover a 30-vertex doubled-G15 external sheet with 60 external edges.
- Both gap-1 orbit representatives pass the layer recoverability audit.
