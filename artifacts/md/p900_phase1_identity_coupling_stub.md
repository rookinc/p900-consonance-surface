# P900 Phase 1 Identity Coupling Stub

Status: sandbox hypothesis

Warning: this is a naive same-index interface rule, not a proven P900 law.

## Rule

For each G15 edge `(s,t)`, couple `(s,x)` to `(t,x)` for every local thalion state `x`.

## Counts

- G15 positions: 15
- G15 edges: 30
- local thalion states per position: 60
- P900 states: 900
- identity coupling edges: 1800
- external degree min: 4
- external degree max: 4
- external degree histogram: {4: 900}

## First read

- The naive identity interface gives every P900 state external degree 4.
- This matches the 4-regularity of G15 = L(Petersen).
- No internal G60 edges are included yet.
- No M or Q interface rule is included yet.

## Next tests

- add internal G60 edge layer from canonical thalion data
- compare identity coupling against M/Q-guided coupling
- test whether total degrees remain disciplined
- test whether thalion identity is preserved under inter-thalion coupling
