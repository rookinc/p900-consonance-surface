# Phase 15 Local Balance Score

Status: sandbox audit

Phase 15 compares the two Phase 13 candidate orbit representatives using per-cycle-length balance.

Both representatives have:

    identity closures: 278
    half-turn closures: 279
    orientation drift: 0
    total balance gap: 1

Tie-breaker:

    local_balance_score = sum over cycle lengths of abs(identity_count - half_turn_count)

Interpretation:

    lower local balance score means the representative distributes identity and half-turn closure more evenly across cycle lengths.

This does not eliminate the other orbit family.
It only selects a preferred representative for the next tests.
