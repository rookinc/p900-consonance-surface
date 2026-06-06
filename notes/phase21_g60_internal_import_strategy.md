# P900 Phase 21 G60 Internal Import Strategy

Status: strategy_checkpoint

Warning: This is an integration plan, not an imported G60 graph and not a closure theorem.

## Current external checkpoint

- p900_vertices: 900
- external_edges: 1800
- external_degree: 4
- external_component_count: 30
- external_component_size: 30
- external_structure: G30-indexed family of identical doubled-G15 sheets
- internal_g60_edges_added: False

## Intended internal import

- address_form: (g15_sector, g60_state)
- rule: For each G15 sector s, add one canonical G60/thalean graph copy on local states x=0..59.
- edge_form: (s,x)--(s,y) whenever x--y is a canonical G60 edge.
- copies: 15
- vertices_per_copy: 60
- expected_edges_per_copy_if_g60_4_regular: 120
- expected_internal_edges_if_g60_4_regular: 1800

## First combined candidate

- vertices: 900
- external_edges: 1800
- expected_internal_edges: 1800
- expected_total_edges: 3600
- expected_degree_if_no_overlap_and_g60_4_regular: 8

## Required source data

- canonical G60 vertex labels 0..59 or a verified label map into 0..59
- canonical G60 edge list
- source provenance for the G60 edge list
- verification that |V|=60 and |E|=120
- verification that the imported G60 copy is the intended thalion / AT4val[60,6] object

## Audit ladder

### Phase 22: canonical_g60_edge_import

- question: Can we import and verify canonical G60 edges with stable local labels 0..59?
- checks:
  - vertex_count_is_60
  - edge_count_is_120
  - degree_histogram_expected
  - connected
  - source_provenance_present

### Phase 23: combined_p900_graph_audit

- question: What is the graph obtained by overlaying 15 internal G60 copies with the preferred external P900 edge law?
- checks:
  - p900_vertex_count_is_900
  - internal_edge_count_is_1800_if_g60_4_regular
  - external_edge_count_is_1800
  - total_edge_count
  - degree_histogram
  - duplicate_edge_count

### Phase 24: closure_component_audit

- question: Do internal G60 edges connect the 30 doubled-G15 external sheets into one object?
- checks:
  - component_count
  - component_size_histogram
  - connected
  - diameter_if_connected
  - sheet_recoverability_after_internal_import

### Phase 25: orbit_family_comparison_after_g60

- question: Does the preferred gap-1 orbit remain preferred after internal G60 edges are added?
- checks:
  - compare_gap1_orbit_1_combined_graph
  - compare_gap1_orbit_2_combined_graph
  - degree_and_component_profiles
  - diameter_profiles
  - closure_profiles

## Safe language

- G60 internal import
- 15 internal thalion copies
- combined P900 candidate
- closure audit
- external scaffold plus internal body

## Avoid language until proven

- P900 is closed
- P900 is the final graph
- 900 proves closure
- the external scaffold alone is the full organism
- the imported object is canonical without provenance

## Working hypothesis

If canonical G60 edges are added inside each of the 15 G15 sectors, the 30 external doubled-G15 sheets may be stitched into a connected 900-state body. This is the next closure test.
