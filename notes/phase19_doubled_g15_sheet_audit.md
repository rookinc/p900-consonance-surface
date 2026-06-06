# Phase 19 Doubled-G15 Sheet Audit

Status: external surface audit

Phase 19 tests whether each Phase 18 component is a doubled G15 sheet.

Within a component indexed by residue r mod 30:

    (s, r)      becomes (s, bit 0)
    (s, r + 30) becomes (s, bit 1)

Then each G15 edge lifts as either:

    parallel edge, if shift is 0
    cross edge, if shift is 30

Question:

    Is each component a 2-lift of G15?

If yes, the preferred external P900 layer is:

    30 identical doubled-G15 sheets

This still does not include internal G60 edges.
