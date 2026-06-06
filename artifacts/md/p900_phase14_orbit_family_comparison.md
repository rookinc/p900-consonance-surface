# P900 Phase 14 Orbit Family Comparison

Status: sandbox audit

Warning: this compares representative split laws from the two preferred orbit families. It does not prove a final P900 law.

## Families

- gap1_orbit_1_representative: [0, 1, 2, 3, 5]
- gap1_orbit_2_representative: [0, 1, 2, 3, 9]

## Total comparison

- cycle count: 557
- same total profile: True
- same length profile: False

### gap1_orbit_1_representative

- half-turn set: [0, 1, 2, 3, 5]
- edge label counts: {'half_turn': 15, 'identity': 15}
- identity closures: 278
- half-turn closures: 279
- orientation drift: 0
- balance gap: 1
- length closure histogram: {'3': {'half_turn_closure': 5, 'identity_closure': 5}, '5': {'half_turn_closure': 6, 'identity_closure': 6}, '6': {'half_turn_closure': 38, 'identity_closure': 32}, '7': {'half_turn_closure': 86, 'identity_closure': 94}, '8': {'half_turn_closure': 144, 'identity_closure': 141}}

### gap1_orbit_2_representative

- half-turn set: [0, 1, 2, 3, 9]
- edge label counts: {'half_turn': 15, 'identity': 15}
- identity closures: 278
- half-turn closures: 279
- orientation drift: 0
- balance gap: 1
- length closure histogram: {'3': {'half_turn_closure': 5, 'identity_closure': 5}, '5': {'half_turn_closure': 6, 'identity_closure': 6}, '6': {'half_turn_closure': 32, 'identity_closure': 38}, '7': {'half_turn_closure': 90, 'identity_closure': 90}, '8': {'half_turn_closure': 146, 'identity_closure': 139}}

## Length-by-length comparison

- length 3: {'gap1_orbit_1_representative': {'half_turn_closure': 5, 'identity_closure': 5}, 'gap1_orbit_2_representative': {'half_turn_closure': 5, 'identity_closure': 5}}
- length 5: {'gap1_orbit_1_representative': {'half_turn_closure': 6, 'identity_closure': 6}, 'gap1_orbit_2_representative': {'half_turn_closure': 6, 'identity_closure': 6}}
- length 6: {'gap1_orbit_1_representative': {'half_turn_closure': 38, 'identity_closure': 32}, 'gap1_orbit_2_representative': {'half_turn_closure': 32, 'identity_closure': 38}}
- length 7: {'gap1_orbit_1_representative': {'half_turn_closure': 86, 'identity_closure': 94}, 'gap1_orbit_2_representative': {'half_turn_closure': 90, 'identity_closure': 90}}
- length 8: {'gap1_orbit_1_representative': {'half_turn_closure': 144, 'identity_closure': 141}, 'gap1_orbit_2_representative': {'half_turn_closure': 146, 'identity_closure': 139}}

## First read

- Phase 14 compares the two preferred gap-1 candidate orbit families.
- Both representatives have total closure balance 278/279 and zero drift.
- The useful question is whether they differ by cycle length profile.
- If the length profiles match, the next discriminator must involve finer cycle records or internal G60 data.
