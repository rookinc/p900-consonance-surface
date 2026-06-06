from pathlib import Path
import json
from itertools import permutations
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

petersen_edge_set = {tuple(sorted(e)) for e in petersen_edges}
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

def closure_profile_for_perm(perm):
    edge_shift = {}

    for a, b in g15_edges:
        shared = shared_vertices[(a, b)]
        relabeled_shared = perm[shared]

        if relabeled_shared % 2 == 0:
            shift = 0
        else:
            shift = 30

        edge_shift[(a, b)] = shift
        edge_shift[(b, a)] = shift

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
        "identity_closure_count": identity_count,
        "half_turn_closure_count": half_count,
        "orientation_drift_count": drift_count,
        "identity_half_turn_balance_gap": abs(identity_count - half_count),
        "holonomy_shift_histogram_mod_60": dict(sorted(holonomy_counter.items())),
        "closure_type_histogram": dict(sorted(closure_counter.items())),
    }

profile_counter = Counter()
profile_examples = {}
profiles = []

for idx, perm in enumerate(automorphisms):
    profile = closure_profile_for_perm(perm)
    key = (
        profile["identity_closure_count"],
        profile["half_turn_closure_count"],
        profile["orientation_drift_count"],
        profile["identity_half_turn_balance_gap"],
    )
    profile_counter[key] += 1
    if key not in profile_examples:
        profile_examples[key] = perm
    profiles.append(profile)

distinct_profiles = []
for key, count in sorted(profile_counter.items(), key=lambda item: (item[0][3], item[0], item[1])):
    identity_count, half_count, drift_count, gap = key
    distinct_profiles.append({
        "identity_closure_count": identity_count,
        "half_turn_closure_count": half_count,
        "orientation_drift_count": drift_count,
        "identity_half_turn_balance_gap": gap,
        "automorphism_count": count,
        "example_permutation": profile_examples[key],
    })

best_gap = min(p["identity_half_turn_balance_gap"] for p in distinct_profiles)
worst_gap = max(p["identity_half_turn_balance_gap"] for p in distinct_profiles)
all_no_drift = all(p["orientation_drift_count"] == 0 for p in profiles)
profile_is_constant = len(distinct_profiles) == 1

summary = {
    "name": "P900 Phase 9 Candidate Law Relabeling Audit",
    "status": "sandbox_audit",
    "warning": "This audits dependence on Petersen vertex labeling. It does not prove an intrinsic P900 law.",
    "candidate_law_under_test": "shared_vertex_parity_binary_consonance",
    "automorphism_count": len(automorphisms),
    "cycle_count": len(cycles),
    "cycle_search_max_length": 8,
    "distinct_profile_count": len(distinct_profiles),
    "profile_is_constant_under_petersen_automorphisms": profile_is_constant,
    "all_profiles_no_orientation_drift": all_no_drift,
    "best_identity_half_turn_balance_gap": best_gap,
    "worst_identity_half_turn_balance_gap": worst_gap,
    "distinct_profiles": distinct_profiles,
    "first_read": [
        "This audit tests whether the candidate parity law is stable under Petersen automorphisms.",
        "Because the law uses odd/even labels, it may depend on the chosen labeling of Petersen vertices.",
        "If the profile is not constant, the current candidate law is coordinate-sensitive.",
        "If all profiles still have zero drift, the binary 0/30 discipline survives relabeling even if balance changes.",
    ],
}

json_path = OUT_JSON / "p900_phase9_candidate_law_relabeling_audit.json"
md_path = OUT_MD / "p900_phase9_candidate_law_relabeling_audit.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 9 Candidate Law Relabeling Audit")
lines.append("")
lines.append("Status: sandbox audit")
lines.append("")
lines.append("Warning: this audits dependence on Petersen vertex labeling. It does not prove an intrinsic P900 law.")
lines.append("")
lines.append("## Candidate law under test")
lines.append("")
lines.append("`shared_vertex_parity_binary_consonance`")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- Petersen automorphisms audited: {summary['automorphism_count']}")
lines.append(f"- cycles audited: {summary['cycle_count']}")
lines.append(f"- distinct closure profiles: {summary['distinct_profile_count']}")
lines.append(f"- profile constant under automorphisms: {summary['profile_is_constant_under_petersen_automorphisms']}")
lines.append(f"- all profiles no orientation drift: {summary['all_profiles_no_orientation_drift']}")
lines.append(f"- best balance gap: {summary['best_identity_half_turn_balance_gap']}")
lines.append(f"- worst balance gap: {summary['worst_identity_half_turn_balance_gap']}")
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Distinct profiles")
lines.append("")
for p in distinct_profiles:
    lines.append(
        "- identity {identity}, half-turn {half}, drift {drift}, gap {gap}, automorphisms {count}".format(
            identity=p["identity_closure_count"],
            half=p["half_turn_closure_count"],
            drift=p["orientation_drift_count"],
            gap=p["identity_half_turn_balance_gap"],
            count=p["automorphism_count"],
        )
    )
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("automorphism_count=" + str(summary["automorphism_count"]))
print("distinct_profile_count=" + str(summary["distinct_profile_count"]))
print("profile_is_constant_under_petersen_automorphisms=" + str(summary["profile_is_constant_under_petersen_automorphisms"]))
print("all_profiles_no_orientation_drift=" + str(summary["all_profiles_no_orientation_drift"]))
print("best_identity_half_turn_balance_gap=" + str(summary["best_identity_half_turn_balance_gap"]))
print("worst_identity_half_turn_balance_gap=" + str(summary["worst_identity_half_turn_balance_gap"]))
print("distinct_profiles:")
for p in distinct_profiles:
    print("identity=" + str(p["identity_closure_count"]) + " half_turn=" + str(p["half_turn_closure_count"]) + " drift=" + str(p["orientation_drift_count"]) + " gap=" + str(p["identity_half_turn_balance_gap"]) + " automorphisms=" + str(p["automorphism_count"]))
