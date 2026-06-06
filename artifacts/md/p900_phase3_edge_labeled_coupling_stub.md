# P900 Phase 3 Edge-Labeled Coupling Stub

Status: sandbox hypothesis

Warning: this is a deterministic stitched-interface baseline, not a proven P900 law.

## Purpose

Phase 3 tests a stitched surface rule where different G15 edges carry different local orientation maps.

## Edge-label pattern

- identity: shift 0 mod 60
- half_turn_plus_30: shift 30 mod 60
- forward_step_plus_1: shift 1 mod 60
- backward_step_minus_1: shift -1 mod 60

## Counts

- G15 positions: 15
- G15 edges: 30
- local thalion states per position: 60
- P900 states: 900
- coupling edges: 1800
- edge label counts: {'backward_step_minus_1': 7, 'forward_step_plus_1': 7, 'half_turn_plus_30': 8, 'identity': 8}
- external degree min: 4
- external degree max: 4
- external degree histogram: {4: 900}
- uniform external degree 4: True

## First read

- The P900 external surface layer remains uniformly degree 4 under a deterministic edge-labeled stitching rule.
- This is less product-like than applying one global local map everywhere.
- The result suggests that G15 adjacency can host heterogeneous local orientation maps without immediate degree collapse.
- No internal G60 edges are included yet.
- No M or Q interface rule is included yet.

## Next tests

- test cycle holonomy around cycles in G15 under edge-labeled shifts
- compare edge-label shift sums against G15 cycle structure
- introduce a half-turn-heavy G30-oriented labeling
- add internal G60 edges when canonical data is available
- compare M-guided and Q-guided interface rules against these baselines
