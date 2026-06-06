# P900 Phase 6 Binary Label Family Audit

Status: sandbox hypothesis

Warning: this compares binary 0/30 label families, not proven P900 laws.

## Purpose

Phase 6 compares several binary G30-style edge-label rules on G15.

Since binary 0/30 labels eliminate orientation drift by construction, the discriminator is identity/half-turn closure balance.

## Ranking

- shared_vertex_odd_half_turn: drift 0, identity 282, half-turn 275, balance gap 7, edge labels {'half_turn': 15, 'identity': 15}
- inner_touch_half_turn: drift 0, identity 286, half-turn 271, balance gap 15, edge labels {'half_turn': 15, 'identity': 15}
- outer_touch_half_turn: drift 0, identity 286, half-turn 271, balance gap 15, edge labels {'half_turn': 15, 'identity': 15}
- alternating_index: drift 0, identity 288, half-turn 269, balance gap 19, edge labels {'half_turn': 15, 'identity': 15}
- all_half_turn: drift 0, identity 355, half-turn 202, balance gap 153, edge labels {'half_turn': 30}
- all_identity: drift 0, identity 557, half-turn 0, balance gap 557, edge labels {'identity': 30}
- different_petersen_edge_type_half_turn: drift 0, identity 557, half-turn 0, balance gap 557, edge labels {'half_turn': 20, 'identity': 10}
- spoke_touch_half_turn: drift 0, identity 557, half-turn 0, balance gap 557, edge labels {'half_turn': 20, 'identity': 10}

## First read

- All binary 0/30 label families eliminate orientation drift by construction.
- The useful discriminator is the identity/half-turn closure balance over G15 cycles.
- Rules with a smaller balance gap distribute identity and half-turn closures more evenly.
- This gives a way to search for a consonance labeling before introducing M or Q.
