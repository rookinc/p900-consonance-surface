# P900 Phase 4 Cycle Holonomy Stub

Status: sandbox hypothesis

Warning: this audits the Phase 3 deterministic edge-label baseline, not a proven P900 law.

## Purpose

Phase 4 audits cycle holonomy around G15 cycles under the Phase 3 stitched edge-label rule.

Interpretation:

- 0 mod 60 means identity closure.
- 30 mod 60 means half-turn closure.
- any other residue means orientation drift.

## Counts

- G15 positions: 15
- G15 edges: 30
- cycle search max length: 8
- cycle count: 557
- cycle length histogram: {3: 10, 5: 12, 6: 70, 7: 180, 8: 285}
- holonomy shift histogram mod 60: {0: 67, 1: 55, 2: 32, 3: 5, 4: 2, 26: 2, 27: 13, 28: 37, 29: 62, 30: 72, 31: 59, 32: 28, 33: 10, 34: 1, 56: 1, 57: 15, 58: 39, 59: 57}
- closure type histogram: {'half_turn_closure': 72, 'identity_closure': 67, 'orientation_drift': 418}

## First read

- Cycle holonomy measures whether stitched local shifts close consistently around G15 cycles.
- 0 mod 60 indicates identity closure.
- 30 mod 60 indicates half-turn closure.
- Other residues indicate orientation drift for this baseline labeling.
- This is the first audit that speaks directly to G15/G30 orientation-restoration intuition.

## Sample records

- cycle [0, 1, 6] length 3 shift 31 closure orientation_drift
- cycle [0, 4, 5] length 3 shift 59 closure orientation_drift
- cycle [1, 2, 7] length 3 shift 59 closure orientation_drift
- cycle [2, 3, 8] length 3 shift 28 closure orientation_drift
- cycle [3, 4, 9] length 3 shift 2 closure orientation_drift
- cycle [5, 10, 14] length 3 shift 0 closure identity_closure
- cycle [6, 12, 13] length 3 shift 29 closure orientation_drift
- cycle [7, 10, 11] length 3 shift 29 closure orientation_drift
- cycle [8, 13, 14] length 3 shift 59 closure orientation_drift
- cycle [9, 11, 12] length 3 shift 58 closure orientation_drift
- cycle [0, 1, 2, 3, 4] length 5 shift 30 closure half_turn_closure
- cycle [0, 1, 7, 10, 5] length 5 shift 0 closure identity_closure
- cycle [0, 4, 9, 12, 6] length 5 shift 2 closure orientation_drift
- cycle [0, 5, 14, 13, 6] length 5 shift 31 closure orientation_drift
- cycle [1, 2, 8, 13, 6] length 5 shift 29 closure orientation_drift
- cycle [1, 6, 12, 11, 7] length 5 shift 0 closure identity_closure
- cycle [2, 3, 9, 11, 7] length 5 shift 58 closure orientation_drift
- cycle [2, 7, 10, 14, 8] length 5 shift 29 closure orientation_drift
- cycle [3, 4, 5, 14, 8] length 5 shift 31 closure orientation_drift
- cycle [3, 8, 13, 12, 9] length 5 shift 29 closure orientation_drift
