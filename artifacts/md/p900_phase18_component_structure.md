# P900 Phase 18 Component Structure Audit

Status: external surface audit

Warning: this audits the external inter-thalion surface only. It does not include internal G60 edges.

## Counts

- component count: 30
- component size histogram: {30: 30}
- local residue mod 30 count histogram: {1: 30}
- all components size 30: True
- all components have 15 sectors: True
- all components have two states per sector: True
- all components single mod 30 residue: True

## First read

- The external-only P900 surface decomposes into 30 equal components.
- Each component should be checked for sector coverage and local-index organization.
- If each component has all 15 sectors with two local states per sector, it is a doubled G15-like sheet.
- If each component is organized by one residue mod 30, the external surface is explicitly G30-indexed.

## First 10 components

### Component 0

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [0]
- local values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

### Component 1

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [1]
- local values: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31]

### Component 2

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [2]
- local values: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]

### Component 3

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [3]
- local values: [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]

### Component 4

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [4]
- local values: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34]

### Component 5

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [5]
- local values: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35]

### Component 6

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [6]
- local values: [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36]

### Component 7

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [7]
- local values: [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37]

### Component 8

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [8]
- local values: [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38]

### Component 9

- size: 30
- sectors present: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
- sector count histogram: {2: 15}
- local residues mod 30: [9]
- local values: [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39]

