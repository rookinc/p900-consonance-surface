# P900 Phase 28 All-Root Shell Profile Comparison

Status: all_root_profiles_distinguish_gap1_orbits

Warning: This compares all-root shell profiles for two closure-bearing candidates. It is not a final selector.

## Comparison

- same_distinct_shell_profile_count: False
- same_eccentricity_histogram: False
- orbit1_distinct_shell_profile_count: 539
- orbit2_distinct_shell_profile_count: 538
- orbit1_eccentricity_histogram: {6: 342, 7: 526, 8: 32}
- orbit2_eccentricity_histogram: {6: 327, 7: 525, 8: 48}

## Candidate summaries

### gap1_orbit_1_representative

- half_turn_set: [0, 1, 2, 3, 5]
- identity_set: [4, 6, 7, 8, 9]
- vertex_count: 900
- combined_edge_count: 3600
- distinct_shell_profile_count: 539
- eccentricity_histogram: {6: 342, 7: 526, 8: 32}

Top shell profiles:

- count 4, example root 53: [1, 8, 36, 121, 272, 309, 129, 24]
- count 2, example root 0: [1, 8, 52, 175, 329, 257, 77, 1]
- count 2, example root 1: [1, 8, 52, 186, 350, 260, 43]
- count 2, example root 2: [1, 8, 52, 204, 370, 242, 23]
- count 2, example root 3: [1, 8, 52, 190, 371, 239, 39]
- count 2, example root 4: [1, 8, 52, 179, 336, 265, 58, 1]
- count 2, example root 5: [1, 8, 52, 186, 364, 259, 30]
- count 2, example root 6: [1, 8, 52, 187, 354, 258, 40]
- count 2, example root 7: [1, 8, 52, 196, 348, 253, 42]
- count 2, example root 8: [1, 8, 52, 187, 347, 264, 41]
- count 2, example root 9: [1, 8, 52, 183, 349, 272, 35]
- count 2, example root 10: [1, 8, 48, 167, 354, 284, 38]

### gap1_orbit_2_representative

- half_turn_set: [0, 1, 2, 3, 9]
- identity_set: [4, 5, 6, 7, 8]
- vertex_count: 900
- combined_edge_count: 3600
- distinct_shell_profile_count: 538
- eccentricity_histogram: {6: 327, 7: 525, 8: 48}

Top shell profiles:

- count 4, example root 413: [1, 8, 34, 106, 241, 321, 155, 34]
- count 2, example root 0: [1, 8, 52, 175, 315, 261, 87, 1]
- count 2, example root 1: [1, 8, 52, 186, 344, 264, 45]
- count 2, example root 2: [1, 8, 52, 204, 364, 246, 25]
- count 2, example root 3: [1, 8, 52, 190, 357, 251, 41]
- count 2, example root 4: [1, 8, 52, 179, 324, 267, 68, 1]
- count 2, example root 5: [1, 8, 52, 186, 350, 267, 36]
- count 2, example root 6: [1, 8, 52, 187, 346, 264, 42]
- count 2, example root 7: [1, 8, 52, 196, 342, 253, 48]
- count 2, example root 8: [1, 8, 52, 187, 339, 268, 45]
- count 2, example root 9: [1, 8, 52, 183, 339, 276, 41]
- count 2, example root 10: [1, 8, 48, 167, 340, 294, 42]

## First read

- Phase 28 computes shell profiles from all 900 roots for both gap-1 orbit representatives.
- This strengthens Phase 25 by replacing sampled-root profiles with complete all-root shell data.
- The all-root profile data distinguishes the two closure-bearing candidates.
