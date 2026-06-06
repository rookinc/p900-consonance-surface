# P900 Phase 22 Canonical G60 Import

Status: import_ok

Warning: This imports the local G60 edge list for P900 use. It does not yet build the combined P900 graph.

## Source

- source path: /data/data/com.termux/files/home/dev/cori/aletheos.ai/public_html/json/at4val_60_6_3d.json
- source name: AT4val[60,6]
- source description: 60-vertex, 120-edge, 4-regular Thalean G60 model.

## Checks

- source_exists: True
- source_name_is_at4val_60_6: True
- vertex_count_is_60: True
- edge_count_is_120: True
- vertices_are_0_to_59: True
- all_edges_are_simple: True
- all_edges_are_in_range: True
- connected: True
- degree_regular_4: True
- root0_shell_profile_matches_memory: True
- root0_diameter_is_6: True

## Counts

- vertex count: 60
- edge count: 120
- degree histogram: {4: 60}
- connected: True
- root 0 shell profile: [1, 4, 8, 16, 24, 6, 1]
- root 0 diameter: 6

## Import rule

Use these 120 edges as the canonical internal G60/thalean edge list on local states 0..59. In P900, each sector s receives edges (s,a)--(s,b) for every imported G60 edge a--b.

## First 30 edges

- [0, 16]
- [0, 19]
- [0, 25]
- [0, 55]
- [1, 15]
- [1, 26]
- [1, 29]
- [1, 35]
- [2, 25]
- [2, 36]
- [2, 39]
- [2, 45]
- [3, 35]
- [3, 46]
- [3, 49]
- [3, 55]
- [4, 15]
- [4, 45]
- [4, 56]
- [4, 59]
- [5, 11]
- [5, 14]
- [5, 20]
- [5, 50]
- [6, 10]
- [6, 21]
- [6, 24]
- [6, 30]
- [7, 20]
- [7, 31]

## Next phase

Phase 23 should overlay 15 internal G60 copies with the preferred Phase 17 external P900 edge list and audit the combined 900-state graph.
