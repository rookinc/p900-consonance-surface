# P900 Phase 2 Orientation Variant Stubs

Status: sandbox hypothesis

Warning: these are simple orientation maps, not proven P900 interface laws.

## Purpose

Phase 1 tested same-index coupling. Phase 2 tests whether the external P900 surface layer remains disciplined under simple local orientation shifts.

## Tested maps

- identity
- half_turn_plus_30
- forward_step_plus_1
- backward_step_minus_1

## Variant summaries

### identity

- edge count: 1800
- external degree min: 4
- external degree max: 4
- external degree histogram: {4: 900}

### half_turn_plus_30

- edge count: 1800
- external degree min: 4
- external degree max: 4
- external degree histogram: {4: 900}

### forward_step_plus_1

- edge count: 1800
- external degree min: 4
- external degree max: 4
- external degree histogram: {4: 900}

### backward_step_minus_1

- edge count: 1800
- external degree min: 4
- external degree max: 4
- external degree histogram: {4: 900}

## First read

- The P900 external surface layer remains degree-disciplined under identity, half-turn, and one-step orientation maps.
- This suggests the G15 surface grammar is not fragile under simple local orientation shifts.
- No internal G60 edges are included yet.
- No M or Q interface rule is included yet.

## Next tests

- test edge-labeled coupling where each G15 edge chooses a distinct local map
- test half-turn maps against the G30 orientation-restoration intuition
- add real internal G60 edges when canonical data is available
- compare M-guided and Q-guided interface rules against these naive baselines
