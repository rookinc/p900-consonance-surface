# P900 Consonance Surface

Status: sandbox hypothesis

Working claim:

P900 is a candidate 15-thalion consonance surface. It is formed by placing one G60 thalion at each G15 sector-position and using the G15 sector grammar to govern inter-thalion adjacency.

Core slogan:

    G60 is the body.
    P900 is the surface where bodies become mutually viewable.

Recursive interpretation:

    At G15, a vertex is a sector-position.
    At G30, a vertex gains orientation-restoration context.
    At G60, a vertex is sustained inside a thalion body.
    At P900, a whole thalion becomes vertex-like again without ceasing to be a body.

Construction target:

    P900 states are pairs (s, x)
    s = G15 sector-position
    x = G60 thalion-state

    15 sector positions * 60 thalion states = 900 P900 states

Initial discipline:

This is not yet a theorem. This directory is a sandbox for testing whether the construction closes cleanly.

Current phase artifacts:

- `artifacts/json/p900_stub_summary.json`
- `artifacts/json/p900_phase1_identity_coupling_stub.json`
- `artifacts/md/p900_phase1_identity_coupling_stub.md`

Open tests:

1. Does the construction preserve internal G60 identity?
2. Does G15 adjacency provide a non-arbitrary inter-thalion grammar?
3. Can M or Q define lawful interfaces between neighboring thalions?
4. Does the resulting 900-state object close without collapse?
5. Is the sphere only a visualization, or does a spherical realization emerge from the construction?

## Current checkpoint: external P900 surface

Status: external-surface sandbox checkpoint

The strongest current artifact-backed statement is:

    The preferred external P900 layer is a G30-indexed family
    of 30 identical doubled-G15 sheets.

This means:

- P900 address space: 15 x 60 = 900 states
- G15 model: L(Petersen)
- preferred representative: gap1_orbit_2_representative
- preferred half-turn set: [0, 1, 2, 3, 9]
- preferred identity set: [4, 5, 6, 7, 8]
- external edges: 1800
- external degree: uniform 4
- external-only component count: 30
- each component has 30 states
- each component contains all 15 G15 sectors
- each component contains two local states per sector
- each component is indexed by one residue modulo 30
- each component is a 2-lift of G15
- each doubled-G15 sheet has 15 cross and 15 parallel lifted edges

Interpretation:

    The external layer is not yet the full P900 body.
    It is a disciplined G30-indexed scaffold awaiting internal G60 thalion structure.

Do not claim yet:

- P900 is a fully constructed thalion-cluster graph.
- The preferred representative is the final P900 law.
- The external layer alone is connected.
- Internal G60 structure has been added.
- P900 has been identified with AT4val[60,6] or any known graph census object.

Key checkpoint artifacts:

- `artifacts/json/p900_phase20_checkpoint_summary.json`
- `artifacts/md/p900_phase20_checkpoint_summary.md`
- `artifacts/json/p900_phase19_doubled_g15_sheet_audit.json`
- `artifacts/md/p900_phase19_doubled_g15_sheet_audit.md`
- `artifacts/json/p900_phase17_external_edge_list.json`
- `artifacts/md/p900_phase17_external_edge_list.md`

Next intended move:

    Prepare an internal G60 import strategy and test whether internal thalion edges connect the 30 doubled-G15 sheets.
