# Phase 9 Candidate Law Relabeling Audit

Status: sandbox audit

Phase 9 tests whether the current candidate law depends on the chosen Petersen vertex labels.

Candidate law under test:

    shared Petersen vertex even -> identity
    shared Petersen vertex odd  -> half-turn

Concern:

    odd/even is not obviously intrinsic to the Petersen graph.

Audit:

    apply all Petersen automorphisms
    recompute the closure profile
    check whether the identity/half-turn balance is stable

Interpretation:

    if profile is constant, the candidate law may be more intrinsic than expected
    if profile changes, the candidate law is coordinate-sensitive
    if all profiles have zero drift, the binary 0/30 discipline survives relabeling
