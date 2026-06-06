from pathlib import Path
import json
from itertools import combinations, permutations
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

petersen_edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
]

petersen_vertices = list(range(10))
petersen_edge_set = {tuple(sorted(e)) for e in petersen_edges}
g15_positions = list(range(15))

g15_edges = []
shared_vertices = {}
for i, e1 in enumerate(petersen_edges):
    for j in range(i + 1, len(petersen_edges)):
        shared = sorted(set(e1).intersection(set(petersen_edges[j])))
        if shared:
            g15_edges.append((i, j))
            shared_vertices[(i, j)] = shared[0]

adj = defaultdict(list)
for a, b in g15_edges:
    adj[a].append(b)
    adj[b].append(a)

for v in adj:
    adj[v] = sorted(adj[v])

def canonical_cycle(cycle):
    n = len(cycle)
    rotations = []
    for seq in (cycle, list(reversed(cycle))):
        for i in range(n):
            rotations.append(tuple(seq[i:] + seq[:i]))
    return min(rotations)

def simple_cycles_upto(max_len):
    found = set()

    def dfs(start, current, path):
        if len(path) > max_len:
            return
        for nxt in adj[current]:
            if nxt == start and len(path) >= 3:
                found.add(canonical_cycle(path[:]))
            elif nxt not in path and len(path) < max_len:
                dfs(start, nxt, path + [nxt])

    for start in g15_positions:
        dfs(start, start, [start])

    return sorted(found, key=lambda c: (len(c), c))

cycles = simple_cycles_upto(8)

def is_automorphism(perm):
    for a, b in petersen_edge_set:
        image = tuple(sorted((perm[a], perm[b])))
        if image not in petersen_edge_set:
            return False
    return True

print("enumerating Petersen automorphisms...")
automorphisms = []
for p in permutations(petersen_vertices):
    perm = {i: p[i] for i in petersen_vertices}
    if is_automorphism(perm):
        automorphisms.append(perm)

def profile_for_half_turn_set(half_turn_set):
    edge_shift = {}
    edge_label_counts = Counter()

    for a, b in g15_edges:
        shared = shared_vertices[(a, b)]
        if shared in half_turn_set:
            shift = 30
            edge_label_counts["half_turn"] += 1
        else:
            shift = 0
            edge_label_counts["identity"] += 1
        edge_shift[(a, b)] = shift
        edge_shift[(b, a)] = shift

    closure_counter = Counter()
    for cyc in cycles:
        shift_sum = 0
        for i in range(len(cyc)):
            a = cyc[i]
            b = cyc[(i + 1) % len(cyc)]
            shift_sum = (shift_sum + edge_shift[(a, b)]) % 60

        if shift_sum == 0:
            closure_counter["identity_closure"] += 1
        elif shift_sum == 30:
            closure_counter["half_turn_closure"] += 1
        else:
            closure_counter["orientation_drift"] += 1

    identity = closure_counter["identity_closure"]
    half = closure_counter["half_turn_closure"]
    drift = closure_counter["orientation_drift"]

    return {
        "identity_closure_count": identity,
        "half_turn_closure_count": half,
        "orientation_drift_count": drift,
        "identity_half_turn_balance_gap": abs(identity - half),
        "edge_label_counts": dict(sorted(edge_label_counts.items())),
        "closure_type_histogram": dict(sorted(closure_counter.items())),
    }

all_sets = {frozenset(s) for s in combinations(petersen_vertices, 5)}

def image_of_set(s, perm):
    return frozenset(perm[x] for x in s)

unseen = set(all_sets)
orbits = []

while unseen:
    seed = min(unseen, key=lambda x: tuple(sorted(x)))
    orbit = {image_of_set(seed, perm) for perm in automorphisms}
    orbit = orbit.intersection(all_sets)

    profiles = [profile_for_half_turn_set(s) for s in orbit]
    gap_counter = Counter(p["identity_half_turn_balance_gap"] for p in profiles)
    profile_counter = Counter(
        (
            p["identity_closure_count"],
            p["half_turn_closure_count"],
            p["orientation_drift_count"],
            p["identity_half_turn_balance_gap"],
            tuple(sorted(p["edge_label_counts"].items())),
        )
        for p in profiles
    )

    representative_profile = profile_for_half_turn_set(seed)

    orbits.append({
        "representative": sorted(seed),
        "orbit_size": len(orbit),
        "gap_histogram": dict(sorted(gap_counter.items())),
        "distinct_profile_count": len(profile_counter),
        "representative_profile": representative_profile,
        "sample_sets": [sorted(s) for s in sorted(orbit, key=lambda x: tuple(sorted(x)))[:10]],
    })

    unseen -= orbit

orbits_sorted = sorted(
    orbits,
    key=lambda o: (
        min(o["gap_histogram"].keys()),
        o["representative"],
    )
)

candidate = frozenset([1, 3, 5, 7, 9])
candidate_orbit_index = None
for idx, orbit in enumerate(orbits_sorted, start=1):
    orbit_sets = {frozenset(s) for s in orbit["sample_sets"]}
    # sample may not include candidate, so recompute from representative.
    rep = frozenset(orbit["representative"])
    full_orbit = {image_of_set(rep, perm) for perm in automorphisms}.intersection(all_sets)
    if candidate in full_orbit:
        candidate_orbit_index = idx
        break

summary = {
    "name": "P900 Phase 11 Vertex Split Orbit Audit",
    "status": "sandbox_audit",
    "warning": "This classifies 5-of-10 Petersen vertex splits under automorphisms. It does not prove a final P900 law.",
    "automorphism_count": len(automorphisms),
    "tested_half_turn_sets": len(all_sets),
    "orbit_count": len(orbits_sorted),
    "candidate_half_turn_set": sorted(candidate),
    "candidate_orbit_rank": candidate_orbit_index,
    "orbits": orbits_sorted,
    "first_read": [
        "Phase 11 groups the 252 half-turn sets into Petersen-automorphism orbits.",
        "This distinguishes intrinsic split families from arbitrary labeled representatives.",
        "If the best gap-1 splits form one or more full orbits, they define candidate consonance families.",
        "The previous odd-vertex split can now be treated as a member of its orbit rather than a privileged label rule."
    ],
}

json_path = OUT_JSON / "p900_phase11_vertex_split_orbits.json"
md_path = OUT_MD / "p900_phase11_vertex_split_orbits.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 11 Vertex Split Orbit Audit")
lines.append("")
lines.append("Status: sandbox audit")
lines.append("")
lines.append("Warning: this classifies 5-of-10 Petersen vertex splits under automorphisms. It does not prove a final P900 law.")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- Petersen automorphisms: {summary['automorphism_count']}")
lines.append(f"- tested half-turn sets: {summary['tested_half_turn_sets']}")
lines.append(f"- orbit count: {summary['orbit_count']}")
lines.append(f"- candidate half-turn set: {summary['candidate_half_turn_set']}")
lines.append(f"- candidate orbit rank: {summary['candidate_orbit_rank']}")
lines.append("")
lines.append("## Orbits")
lines.append("")
for idx, orbit in enumerate(orbits_sorted, start=1):
    prof = orbit["representative_profile"]
    lines.append(f"### Orbit {idx}")
    lines.append("")
    lines.append(f"- representative: {orbit['representative']}")
    lines.append(f"- orbit size: {orbit['orbit_size']}")
    lines.append(f"- gap histogram: {orbit['gap_histogram']}")
    lines.append(f"- distinct profile count: {orbit['distinct_profile_count']}")
    lines.append(f"- representative identity closures: {prof['identity_closure_count']}")
    lines.append(f"- representative half-turn closures: {prof['half_turn_closure_count']}")
    lines.append(f"- representative drift: {prof['orientation_drift_count']}")
    lines.append(f"- representative balance gap: {prof['identity_half_turn_balance_gap']}")
    lines.append(f"- representative edge labels: {prof['edge_label_counts']}")
    lines.append(f"- sample sets: {orbit['sample_sets']}")
    lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("automorphism_count=" + str(summary["automorphism_count"]))
print("tested_half_turn_sets=" + str(summary["tested_half_turn_sets"]))
print("orbit_count=" + str(summary["orbit_count"]))
print("candidate_orbit_rank=" + str(summary["candidate_orbit_rank"]))
print("orbits:")
for idx, orbit in enumerate(orbits_sorted, start=1):
    prof = orbit["representative_profile"]
    print("orbit=" + str(idx) + " representative=" + str(orbit["representative"]) + " size=" + str(orbit["orbit_size"]) + " gap_histogram=" + str(orbit["gap_histogram"]) + " profile_gap=" + str(prof["identity_half_turn_balance_gap"]) + " identity=" + str(prof["identity_closure_count"]) + " half_turn=" + str(prof["half_turn_closure_count"]) + " drift=" + str(prof["orientation_drift_count"]) + " edge_labels=" + str(prof["edge_label_counts"]))
