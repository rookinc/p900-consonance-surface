# Current Status: P900 Consonance Surface

Status: connected candidate checkpoint

This directory records an artifact-backed computational pipeline for a 900-state
P900 consonance surface candidate.

It is not a theorem and does not select a final P900 law.

## Current construction state

The construction begins with the address space:

    P900 states = (s, x)
    s = G15 sector-position
    x = G60 thalion-state

Thus:

    15 * 60 = 900 states

The external layer uses the G15 sector grammar to connect thalion-position
fibers. The internal layer imports one canonical G60 thalion body into each
G15 sector fiber.

## Main checkpoint

The strongest current artifact-backed statement is:

    The preferred external P900 scaffold, when combined with internal G60
    thalion bodies, produces connected 900-state body-plus-surface graph
    candidates.

The combined candidates have:

    vertices: 900
    internal edges: 1800
    external edges: 1800
    combined edges: 3600
    duplicate edges: 0
    degree: uniform 8
    connected: true
    diameter: 8

## Candidate status

Two gap-1 orbit representatives remain closure-bearing after G60 import.

### gap1_orbit_1_representative

Role:

    global-tightness candidate

Half-turn set:

    [0, 1, 2, 3, 5]

Identity set:

    [4, 6, 7, 8, 9]

It wins the crude global tightness criterion:

    fewer diameter-8 vertices
    more eccentricity-6 vertices

### gap1_orbit_2_representative

Role:

    local-balance provisional selector

Half-turn set:

    [0, 1, 2, 3, 9]

Identity set:

    [4, 5, 6, 7, 8]

It wins the local balance criteria and the Phase 27 multi-invariant selector.

## Selector position

The project should not claim a final P900 law.

Current safe language:

    closure-bearing gap-1 family
    connected P900 candidates
    body-plus-surface graph checkpoint
    provisional selector
    local-balance candidate
    global-tightness candidate
    renderer-export-ready graph candidates

Avoid language:

    final P900 theorem
    unique P900 graph
    canonical P900 law
    proof that Orbit 1 is final
    proof that Orbit 2 is final
    metaphysical closure

## Layer recoverability

Both closure-bearing candidates pass the layer recoverability audit.

Recovered layers include:

    G15 sector fibers
    internal G60 copies
    G30 residue sheets
    internal edge class
    external half-turn mod30 edge class
    external identity same-local edge class

This means the overlay does not erase the known address grammar.

## Renderer status

Phase 30 exports both closure-bearing candidates for renderer integration.

Available views:

    combined
    internal_g60
    external_p900
    residue_sheets
    sector_fibers

Default candidate:

    gap1_orbit_2_representative

The renderer export is useful for inspection, but it does not select a final
law by itself.

## Relation to neighboring papers

This project came out of sequence relative to the observed-closure and finite
projection-separation papers.

Current interpretation:

    14-p900-consonance-surface is a computational witness surface.
    13-observed-closure supplies the criterion vocabulary.
    15-finite-projection-separation proves that the stages of admissibility are
    strictly separable.

The P900 pipeline should therefore be read through the newer observed-closure
discipline:

    projection displays
    observation closes
    witness admits

P900 currently has strong projection and closure-style artifacts. It should not
be treated as admitted final structure until the selector and witness predicates
are made explicit.
