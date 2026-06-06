# P900 Phase 25 Gap-1 Orbits After G60

Status: gap1_orbits_both_close_but_differ_after_g60

Warning: This is a basic combined-graph comparison. It does not prove uniqueness or finality.

## Purpose

Compare the two Phase 13 gap-1 orbit representatives after internal G60 import.

## Comparison

- both_connected: True
- same_degree_histogram: True
- same_combined_edge_count: True
- same_diameter: True
- same_eccentricity_histogram: False
- diameters: {'gap1_orbit_1_representative': 8, 'gap1_orbit_2_representative': 8}
- eccentricity_histograms: {'gap1_orbit_1_representative': {6: 342, 7: 526, 8: 32}, 'gap1_orbit_2_representative': {6: 327, 7: 525, 8: 48}}

## Candidate audits

### gap1_orbit_1_representative

- half_turn_set: [0, 1, 2, 3, 5]
- identity_set: [4, 6, 7, 8, 9]
- edge_label_counts: {'half_turn': 15, 'identity': 15}
- vertex_count: 900
- internal_edge_count: 1800
- external_edge_count: 1800
- duplicate_edge_count: 0
- combined_edge_count: 3600
- degree_histogram: {8: 900}
- component_count: 1
- component_size_histogram: {900: 1}
- connected: True
- diameter_if_connected: 8
- eccentricity_histogram: {6: 342, 7: 526, 8: 32}
- sample_root_shell_profiles: {'0': [1, 8, 52, 175, 329, 257, 77, 1], '1': [1, 8, 52, 186, 350, 260, 43], '30': [1, 8, 52, 200, 329, 238, 72], '59': [1, 8, 52, 175, 336, 270, 57, 1], '60': [1, 8, 52, 175, 329, 257, 77, 1], '420': [1, 8, 42, 141, 307, 301, 99, 1], '899': [1, 8, 42, 143, 302, 306, 97, 1]}

### gap1_orbit_2_representative

- half_turn_set: [0, 1, 2, 3, 9]
- identity_set: [4, 5, 6, 7, 8]
- edge_label_counts: {'half_turn': 15, 'identity': 15}
- vertex_count: 900
- internal_edge_count: 1800
- external_edge_count: 1800
- duplicate_edge_count: 0
- combined_edge_count: 3600
- degree_histogram: {8: 900}
- component_count: 1
- component_size_histogram: {900: 1}
- connected: True
- diameter_if_connected: 8
- eccentricity_histogram: {6: 327, 7: 525, 8: 48}
- sample_root_shell_profiles: {'0': [1, 8, 52, 175, 315, 261, 87, 1], '1': [1, 8, 52, 186, 344, 264, 45], '30': [1, 8, 52, 200, 327, 232, 80], '59': [1, 8, 52, 175, 324, 274, 65, 1], '60': [1, 8, 52, 174, 324, 255, 82, 4], '420': [1, 8, 42, 142, 308, 297, 101, 1], '899': [1, 8, 32, 105, 253, 342, 146, 13]}

## First read

- Both gap-1 orbit representatives are tested after adding the same 15 internal canonical G60 copies.
- This checks whether Phase 24 closure is unique to the preferred representative or generic across the two best external orbit families.
- Both representatives produce connected combined P900 graphs.
- The basic global distance profile distinguishes the two representatives.
