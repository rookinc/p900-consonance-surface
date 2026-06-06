# P900 Phase 9 Candidate Law Relabeling Audit

Status: sandbox audit

Warning: this audits dependence on Petersen vertex labeling. It does not prove an intrinsic P900 law.

## Candidate law under test

`shared_vertex_parity_binary_consonance`

## Counts

- Petersen automorphisms audited: 120
- cycles audited: 557
- distinct closure profiles: 1
- profile constant under automorphisms: True
- all profiles no orientation drift: True
- best balance gap: 7
- worst balance gap: 7

## First read

- This audit tests whether the candidate parity law is stable under Petersen automorphisms.
- Because the law uses odd/even labels, it may depend on the chosen labeling of Petersen vertices.
- If the profile is not constant, the current candidate law is coordinate-sensitive.
- If all profiles still have zero drift, the binary 0/30 discipline survives relabeling even if balance changes.

## Distinct profiles

- identity 282, half-turn 275, drift 0, gap 7, automorphisms 120
