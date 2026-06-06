# Phase 2 Orientation Variant Stubs

Status: sandbox hypothesis

Phase 1 tested same-index coupling:

    (s, x) -> (t, x)

Phase 2 tests simple local orientation maps:

    identity: x -> x
    half-turn: x -> x + 30 mod 60
    forward-step: x -> x + 1 mod 60
    backward-step: x -> x - 1 mod 60

The purpose is not to prove a P900 law.

The purpose is to test whether the G15 surface grammar remains degree-disciplined under simple local orientation shifts.

If all variants keep uniform external degree 4, then the surface grammar is not fragile under these basic maps.
