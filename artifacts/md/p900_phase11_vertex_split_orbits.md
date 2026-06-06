# P900 Phase 11 Vertex Split Orbit Audit

Status: sandbox audit

Warning: this classifies 5-of-10 Petersen vertex splits under automorphisms. It does not prove a final P900 law.

## Counts

- Petersen automorphisms: 120
- tested half-turn sets: 252
- orbit count: 6
- candidate half-turn set: [1, 3, 5, 7, 9]
- candidate orbit rank: 3

## Orbits

### Orbit 1

- representative: [0, 1, 2, 3, 5]
- orbit size: 60
- gap histogram: {1: 60}
- distinct profile count: 1
- representative identity closures: 278
- representative half-turn closures: 279
- representative drift: 0
- representative balance gap: 1
- representative edge labels: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 2, 3, 5], [0, 1, 2, 3, 8], [0, 1, 2, 4, 7], [0, 1, 2, 4, 9], [0, 1, 2, 5, 8], [0, 1, 2, 7, 9], [0, 1, 3, 4, 6], [0, 1, 3, 4, 8], [0, 1, 3, 5, 8], [0, 1, 3, 6, 8]]

### Orbit 2

- representative: [0, 1, 2, 3, 9]
- orbit size: 60
- gap histogram: {1: 60}
- distinct profile count: 1
- representative identity closures: 278
- representative half-turn closures: 279
- representative drift: 0
- representative balance gap: 1
- representative edge labels: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 2, 3, 9], [0, 1, 2, 4, 8], [0, 1, 2, 5, 9], [0, 1, 2, 7, 8], [0, 1, 3, 4, 7], [0, 1, 3, 5, 6], [0, 1, 3, 5, 7], [0, 1, 3, 6, 9], [0, 1, 4, 6, 7], [0, 1, 4, 8, 9]]

### Orbit 3

- representative: [0, 1, 2, 8, 9]
- orbit size: 30
- gap histogram: {7: 30}
- distinct profile count: 1
- representative identity closures: 282
- representative half-turn closures: 275
- representative drift: 0
- representative balance gap: 7
- representative edge labels: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 2, 8, 9], [0, 1, 3, 5, 9], [0, 1, 3, 6, 7], [0, 1, 4, 7, 8], [0, 2, 3, 6, 7], [0, 2, 3, 8, 9], [0, 2, 4, 5, 6], [0, 2, 4, 8, 9], [0, 2, 5, 8, 9], [0, 2, 6, 8, 9]]

### Orbit 4

- representative: [0, 1, 3, 7, 8]
- orbit size: 30
- gap histogram: {7: 30}
- distinct profile count: 1
- representative identity closures: 282
- representative half-turn closures: 275
- representative drift: 0
- representative balance gap: 7
- representative edge labels: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 3, 7, 8], [0, 1, 3, 7, 9], [0, 1, 3, 8, 9], [0, 1, 7, 8, 9], [0, 2, 3, 5, 6], [0, 2, 3, 5, 9], [0, 2, 3, 6, 9], [0, 2, 4, 6, 7], [0, 2, 4, 6, 8], [0, 2, 4, 7, 8]]

### Orbit 5

- representative: [0, 1, 2, 3, 4]
- orbit size: 12
- gap histogram: {15: 12}
- distinct profile count: 1
- representative identity closures: 286
- representative half-turn closures: 271
- representative drift: 0
- representative balance gap: 15
- representative edge labels: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 2, 3, 4], [0, 1, 2, 5, 7], [0, 1, 4, 6, 9], [0, 1, 5, 6, 8], [0, 3, 4, 5, 8], [0, 4, 5, 7, 9], [1, 2, 3, 6, 8], [1, 2, 6, 7, 9], [2, 3, 4, 7, 9], [2, 3, 5, 7, 8]]

### Orbit 6

- representative: [0, 1, 2, 3, 6]
- orbit size: 60
- gap histogram: {17: 60}
- distinct profile count: 1
- representative identity closures: 270
- representative half-turn closures: 287
- representative drift: 0
- representative balance gap: 17
- representative edge labels: {'half_turn': 15, 'identity': 15}
- sample sets: [[0, 1, 2, 3, 6], [0, 1, 2, 3, 7], [0, 1, 2, 4, 5], [0, 1, 2, 4, 6], [0, 1, 2, 5, 6], [0, 1, 2, 6, 7], [0, 1, 2, 6, 8], [0, 1, 2, 6, 9], [0, 1, 3, 4, 5], [0, 1, 3, 4, 9]]

## First read

- Phase 11 groups the 252 half-turn sets into Petersen-automorphism orbits.
- This distinguishes intrinsic split families from arbitrary labeled representatives.
- If the best gap-1 splits form one or more full orbits, they define candidate consonance families.
- The previous odd-vertex split can now be treated as a member of its orbit rather than a privileged label rule.
