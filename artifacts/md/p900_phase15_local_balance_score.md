# P900 Phase 15 Local Balance Score

Status: sandbox audit

Warning: this selects a preferred representative by local balance score only. It does not prove a final P900 law.

## Scoring rule

For each candidate family, sum abs(identity_closure - half_turn_closure) across each cycle length.

## Ranking

### Rank 1: gap1_orbit_2_representative

- half-turn set: [0, 1, 2, 3, 9]
- total identity closures: 278
- total half-turn closures: 279
- total orientation drift: 0
- total balance gap: 1
- local balance score: 13
- max length gap: 7
- perfectly balanced length count: 3
- per-length scores: {'3': {'identity_closure': 5, 'half_turn_closure': 5, 'orientation_drift': 0, 'length_balance_gap': 0}, '5': {'identity_closure': 6, 'half_turn_closure': 6, 'orientation_drift': 0, 'length_balance_gap': 0}, '6': {'identity_closure': 38, 'half_turn_closure': 32, 'orientation_drift': 0, 'length_balance_gap': 6}, '7': {'identity_closure': 90, 'half_turn_closure': 90, 'orientation_drift': 0, 'length_balance_gap': 0}, '8': {'identity_closure': 139, 'half_turn_closure': 146, 'orientation_drift': 0, 'length_balance_gap': 7}}

### Rank 2: gap1_orbit_1_representative

- half-turn set: [0, 1, 2, 3, 5]
- total identity closures: 278
- total half-turn closures: 279
- total orientation drift: 0
- total balance gap: 1
- local balance score: 17
- max length gap: 8
- perfectly balanced length count: 2
- per-length scores: {'3': {'identity_closure': 5, 'half_turn_closure': 5, 'orientation_drift': 0, 'length_balance_gap': 0}, '5': {'identity_closure': 6, 'half_turn_closure': 6, 'orientation_drift': 0, 'length_balance_gap': 0}, '6': {'identity_closure': 32, 'half_turn_closure': 38, 'orientation_drift': 0, 'length_balance_gap': 6}, '7': {'identity_closure': 94, 'half_turn_closure': 86, 'orientation_drift': 0, 'length_balance_gap': 8}, '8': {'identity_closure': 141, 'half_turn_closure': 144, 'orientation_drift': 0, 'length_balance_gap': 3}}

## Preferred by local balance

- family: gap1_orbit_2_representative
- half-turn set: [0, 1, 2, 3, 9]
- local balance score: 13

## First read

- Both preferred orbit representatives remain tied at total balance gap 1 with zero drift.
- Phase 15 breaks the tie using local balance by cycle length.
- The lower local balance score is preferred as a representative for the next external-surface tests.
- This does not eliminate the other orbit family.
