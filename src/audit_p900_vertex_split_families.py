from pathlib import Path
import json
from itertools import combinations
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

def closure_profile_for_half_turn_set(half_turn_set):
    edge_shift = {}
    edge_label_counts = Counter()

    for a, b in g15_edges:
        shared = shared_vertices[(a, b)]
        if shared in half_turn_set:
            shift = 30
            label = "half_turn"
        else:
            shift = 0
            label = "identity"

        edge_shift[(a, b)] = shift
        edge_shift[(b, a)] = shift
        edge_label_counts[label] += 1

    closure_counter = Counter()
    holonomy_counter = Counter()

    for cyc in cycles:
        shift_sum = 0
        for i in range(len(cyc)):
            a = cyc[i]
            b = cyc[(i + 1) % len(cyc)]
            shift_sum = (shift_sum + edge_shift[(a, b)]) % 60

        holonomy_counter[shift_sum] += 1

        if shift_sum == 0:
            closure_counter["identity_closure"] += 1
        elif shift_sum == 30:
            closure_counter["half_turn_closure"] += 1
        else:
            closure_counter["orientation_drift"] += 1

    identity_count = closure_counter["identity_closure"]
    half_count = closure_counter["half_turn_closure"]
    drift_count = closure_counter["orientation_drift"]

    return {
        "half_turn_set": sorted(half_turn_set),
        "edge_label_counts": dict(sorted(edge_label_counts.items())),
        "identity_closure_count": identity_count,
        "half_turn_closure_count": half_count,
        "orientation_drift_count": drift_count,
        "identity_half_turn_balance_gap": abs(identity_count - half_count),
        "holonomy_shift_histogram_mod_60": dict(sorted(holonomy_counter.items())),
        "closure_type_histogram": dict(sorted(closure_counter.items())),
    }

profiles = []
for subset in combinations(petersen_vertices, 5):
    profiles.append(closure_profile_for_half_turn_set(set(subset)))

profiles_sorted = sorted(
    profiles,
    key=lambda p: (
        p["orientation_drift_count"],
        p["identity_half_turn_balance_gap"],
        p["half_turn_set"],
    ),
)

gap_counter = Counter(p["identity_half_turn_balance_gap"] for p in profiles)
edge_count_counter = Counter(
    tuple(sorted(p["edge_label_counts"].items()))
    for p in profiles
)

candidate_set = [1, 3, 5, 7, 9]
candidate_profile = None
for p in profiles:
    if p["half_turn_set"] == candidate_set:
        candidate_profile = p
        break

best_gap = profiles_sorted[0]["identity_half_turn_balance_gap"]
best_profiles = [p for p in profiles_sorted if p["identity_half_turn_balance_gap"] == best_gap]
candidate_rank = 1 + profiles_sorted.index(candidate_profile)

summary = {
    "name": "P900 Phase 10 Vertex Split Family Audit",
    "status": "sandbox_audit",
    "warning": "This compares 5-and-5 Petersen vertex splits as binary half-turn sets. It does not prove a final P900 law.",
    "cycle_search_max_length": 8,
    "cycle_count": len(cycles),
    "tested_half_turn_sets": len(profiles),
    "best_identity_half_turn_balance_gap": best_gap,
    "best_profile_count": len(best_profiles),
    "candidate_half_turn_set": candidate_set,
    "candidate_rank": candidate_rank,
    "candidate_profile": candidate_profile,
    "gap_histogram": dict(sorted(gap_counter.items())),
    "edge_label_count_histogram": {
        str(k): v for k, v in sorted(edge_count_counter.items(), key=lambda item: str(item[0]))
    },
    "top_profiles": profiles_sorted[:20],
    "first_read": [
        "Phase 10 tests whether the candidate odd-vertex half-turn set is special among all 5-of-10 Petersen vertex splits.",
        "Every 5-set is used as a half-turn set; its complement is identity.",
        "The discriminator is the identity/half-turn closure balance over audited G15 cycles.",
        "A low rank means the candidate split is not merely arbitrary."
    ],
}

json_path = OUT_JSON / "p900_phase10_vertex_split_families.json"
md_path = OUT_MD / "p900_phase10_vertex_split_families.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 10 Vertex Split Family Audit")
lines.append("")
lines.append("Status: sandbox audit")
lines.append("")
lines.append("Warning: this compares 5-and-5 Petersen vertex splits as binary half-turn sets. It does not prove a final P900 law.")
lines.append("")
lines.append("## Purpose")
lines.append("")
lines.append("Phase 10 asks whether the candidate odd-vertex half-turn set is special among all 5-of-10 Petersen vertex splits.")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- cycles audited: {summary['cycle_count']}")
lines.append(f"- tested half-turn sets: {summary['tested_half_turn_sets']}")
lines.append(f"- best balance gap: {summary['best_identity_half_turn_balance_gap']}")
lines.append(f"- best profile count: {summary['best_profile_count']}")
lines.append(f"- candidate half-turn set: {summary['candidate_half_turn_set']}")
lines.append(f"- candidate rank: {summary['candidate_rank']}")
lines.append(f"- candidate profile: {summary['candidate_profile']}")
lines.append("")
lines.append("## Gap histogram")
lines.append("")
for gap, count in sorted(gap_counter.items()):
    lines.append(f"- gap {gap}: {count}")
lines.append("")
lines.append("## Top profiles")
lines.append("")
for idx, p in enumerate(profiles_sorted[:20], start=1):
    lines.append(
        f"- rank {idx}: set {p['half_turn_set']}, "
        f"identity {p['identity_closure_count']}, "
        f"half-turn {p['half_turn_closure_count']}, "
        f"drift {p['orientation_drift_count']}, "
        f"gap {p['identity_half_turn_balance_gap']}, "
        f"edge labels {p['edge_label_counts']}"
    )
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("tested_half_turn_sets=" + str(summary["tested_half_turn_sets"]))
print("best_identity_half_turn_balance_gap=" + str(summary["best_identity_half_turn_balance_gap"]))
print("best_profile_count=" + str(summary["best_profile_count"]))
print("candidate_half_turn_set=" + str(summary["candidate_half_turn_set"]))
print("candidate_rank=" + str(summary["candidate_rank"]))
print("candidate_profile=" + str(summary["candidate_profile"]))
print("top_profiles:")
for idx, p in enumerate(profiles_sorted[:10], start=1):
    print("rank=" + str(idx) + " set=" + str(p["half_turn_set"]) + " identity=" + str(p["identity_closure_count"]) + " half_turn=" + str(p["half_turn_closure_count"]) + " drift=" + str(p["orientation_drift_count"]) + " gap=" + str(p["identity_half_turn_balance_gap"]) + " edge_labels=" + str(p["edge_label_counts"]))
