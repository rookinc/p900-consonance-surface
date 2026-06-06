# P900 Phase 5 Binary Half-Turn Holonomy

Status: sandbox hypothesis

Warning: this is a binary 0/30 baseline, not a proven P900 law.

## Purpose

Phase 5 tests a G30-style sign grammar where each G15 edge carries either identity shift 0 or half-turn shift 30.

## Counts

- G15 positions: 15
- G15 edges: 30
- P900 states: 900
- coupling edges: 1800
- external degree min: 4
- external degree max: 4
- external degree histogram: {4: 900}
- cycle search max length: 8
- cycle count: 557
- cycle length histogram: {3: 10, 5: 12, 6: 70, 7: 180, 8: 285}
- holonomy shift histogram mod 60: {0: 288, 30: 269}
- closure type histogram: {'half_turn_closure': 269, 'identity_closure': 288}

## First read

- The binary 0/30 interface preserves uniform external degree 4.
- All audited cycles close as either identity or half-turn.
- This eliminates orientation drift by restricting local shifts to the G30-style sign grammar.
- This is a clean baseline for the 360/180/360 intuition.

## Sample records

- cycle [0, 1, 6] length 3 shift 0 closure identity_closure
- cycle [0, 4, 5] length 3 shift 0 closure identity_closure
- cycle [1, 2, 7] length 3 shift 0 closure identity_closure
- cycle [2, 3, 8] length 3 shift 30 closure half_turn_closure
- cycle [3, 4, 9] length 3 shift 0 closure identity_closure
- cycle [5, 10, 14] length 3 shift 30 closure half_turn_closure
- cycle [6, 12, 13] length 3 shift 30 closure half_turn_closure
- cycle [7, 10, 11] length 3 shift 0 closure identity_closure
- cycle [8, 13, 14] length 3 shift 0 closure identity_closure
- cycle [9, 11, 12] length 3 shift 0 closure identity_closure
- cycle [0, 1, 2, 3, 4] length 5 shift 0 closure identity_closure
- cycle [0, 1, 7, 10, 5] length 5 shift 0 closure identity_closure
- cycle [0, 4, 9, 12, 6] length 5 shift 30 closure half_turn_closure
- cycle [0, 5, 14, 13, 6] length 5 shift 0 closure identity_closure
- cycle [1, 2, 8, 13, 6] length 5 shift 30 closure half_turn_closure
- cycle [1, 6, 12, 11, 7] length 5 shift 30 closure half_turn_closure
- cycle [2, 3, 9, 11, 7] length 5 shift 0 closure identity_closure
- cycle [2, 7, 10, 14, 8] length 5 shift 0 closure identity_closure
- cycle [3, 4, 5, 14, 8] length 5 shift 0 closure identity_closure
- cycle [3, 8, 13, 12, 9] length 5 shift 0 closure identity_closure
