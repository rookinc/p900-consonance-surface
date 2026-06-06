# P900 Phase 13 Candidate Orbit Families

Status: candidate family checkpoint

Warning: this promotes candidate orbit families, not a final theorem or final P900 construction.

## Selection rule

Choose Petersen 5-vertex split orbits with minimal identity/half-turn balance gap among tested 5-of-10 binary half-turn sets.

## Result

- best balance gap: 1
- candidate family count: 2

## Candidate families

### gap1_orbit_1

- representative half-turn set: [0, 1, 2, 3, 5]
- orbit size: 60
- identity closures: 278
- half-turn closures: 279
- orientation drift: 0
- balance gap: 1
- edge label counts: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 2, 3, 5], [0, 1, 2, 3, 8], [0, 1, 2, 4, 7], [0, 1, 2, 4, 9], [0, 1, 2, 5, 8], [0, 1, 2, 7, 9], [0, 1, 3, 4, 6], [0, 1, 3, 4, 8], [0, 1, 3, 5, 8], [0, 1, 3, 6, 8]]

### gap1_orbit_2

- representative half-turn set: [0, 1, 2, 3, 9]
- orbit size: 60
- identity closures: 278
- half-turn closures: 279
- orientation drift: 0
- balance gap: 1
- edge label counts: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 2, 3, 9], [0, 1, 2, 4, 8], [0, 1, 2, 5, 9], [0, 1, 2, 7, 8], [0, 1, 3, 4, 7], [0, 1, 3, 5, 6], [0, 1, 3, 5, 7], [0, 1, 3, 6, 9], [0, 1, 4, 6, 7], [0, 1, 4, 8, 9]]

## Working position

- P900 binary consonance is currently best treated as an orbit-family problem.
- The preferred candidates are the two Petersen split orbits with balance gap 1.
- The old odd/even parity law remains a stable baseline but is no longer preferred.
- All candidate families preserve binary 0/30 drift-free closure over the audited G15 cycles.
- No internal G60 data has been added yet.

## Next tests

- choose one representative from each gap-1 orbit and build explicit edge-law tables
- compare orbit 1 and orbit 2 cycle length closure profiles
- test whether orbit 1 and orbit 2 are complements or structurally distinct under the audit
- add internal G60 data only after the external orbit-family layer is checkpointed
