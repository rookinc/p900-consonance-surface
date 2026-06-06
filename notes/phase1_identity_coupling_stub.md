# Phase 1 Identity Coupling Stub

Status: sandbox hypothesis

This phase adds the first inter-thalion coupling rule.

It does not use the internal G60 graph yet.

It does not use M or Q yet.

## Rule

If two G15 sector-positions are adjacent, then corresponding local thalion states may couple by shared local index.

In address form:

    (s, x) couples to (t, x)

whenever:

    s -- t in G15 = L(Petersen)

## Why this rule is useful

This is the smallest nontrivial surface-coupling test.

It checks whether G15 adjacency can lift across 60 local thalion states without exploding the degree structure.

## Expected count

G15 has 30 edges.

Each G15 edge lifts across 60 local states.

So the naive identity interface has:

    30 * 60 = 1800

inter-thalion coupling edges.

Since G15 is 4-regular, each P900 state should have external degree 4 under this rule.

## Caution

This is not the final P900 law.

It is a baseline interface stub to compare against future M-guided and Q-guided coupling rules.
