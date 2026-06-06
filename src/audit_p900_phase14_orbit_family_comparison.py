from pathlib import Path
import json
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

families = {
    "gap1_orbit_1_representative": [0, 1, 2, 3, 5],
    "gap1_orbit_2_representative": [0, 1, 2, 3, 9],
}

def profile_for_set(half_turn_set):
    half_turn_set = set(half_turn_set)
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
    length_closure = defaultdict(Counter)
    records = []

    for cyc in cycles:
        shift_sum = 0
        shared_sequence = []
        for i in range(len(cyc)):
            a = cyc[i]
            b = cyc[(i + 1) % len(cyc)]
            shared = shared_vertices[(min(a, b), max(a, b))]
            shared_sequence.append(shared)
            shift_sum = (shift_sum + edge_shift[(a, b)]) % 60

        if shift_sum == 0:
            closure_type = "identity_closure"
        elif shift_sum == 30:
            closure_type = "half_turn_closure"
        else:
            closure_type = "orientation_drift"

        closure_counter[closure_type] += 1
        length_closure[str(len(cyc))][closure_type] += 1

        records.append({
            "cycle": list(cyc),
            "length": len(cyc),
            "shared_vertex_sequence": shared_sequence,
            "shift_sum_mod_60": shift_sum,
            "closure_type": closure_type,
        })

    identity = closure_counter["identity_closure"]
    half = closure_counter["half_turn_closure"]
    drift = closure_counter["orientation_drift"]

    return {
        "half_turn_set": sorted(half_turn_set),
        "edge_label_counts": dict(sorted(edge_label_counts.items())),
        "identity_closure_count": identity,
        "half_turn_closure_count": half,
        "orientation_drift_count": drift,
        "identity_half_turn_balance_gap": abs(identity - half),
        "closure_type_histogram": dict(sorted(closure_counter.items())),
        "length_closure_histogram": {
            k: dict(sorted(v.items()))
            for k, v in sorted(length_closure.items(), key=lambda item: int(item[0]))
        },
        "records": records,
    }

profiles = {name: profile_for_set(s) for name, s in families.items()}

diff_by_length = {}
lengths = sorted({k for p in profiles.values() for k in p["length_closure_histogram"].keys()}, key=int)

for length in lengths:
    row = {}
    for name, p in profiles.items():
        row[name] = p["length_closure_histogram"].get(length, {})
    diff_by_length[length] = row

same_length_profile = (
    profiles["gap1_orbit_1_representative"]["length_closure_histogram"]
    == profiles["gap1_orbit_2_representative"]["length_closure_histogram"]
)

same_total_profile = (
    profiles["gap1_orbit_1_representative"]["closure_type_histogram"]
    == profiles["gap1_orbit_2_representative"]["closure_type_histogram"]
)

summary = {
    "name": "P900 Phase 14 Orbit Family Comparison",
    "status": "sandbox_audit",
    "warning": "This compares representative split laws from the two preferred orbit families. It does not prove a final P900 law.",
    "cycle_count": len(cycles),
    "cycle_search_max_length": 8,
    "families": families,
    "profiles": {
        k: {kk: vv for kk, vv in v.items() if kk != "records"}
        for k, v in profiles.items()
    },
    "same_total_profile": same_total_profile,
    "same_length_profile": same_length_profile,
    "diff_by_length": diff_by_length,
    "first_read": [
        "Phase 14 compares the two preferred gap-1 candidate orbit families.",
        "Both representatives have total closure balance 278/279 and zero drift.",
        "The useful question is whether they differ by cycle length profile.",
        "If the length profiles match, the next discriminator must involve finer cycle records or internal G60 data."
    ],
}

json_path = OUT_JSON / "p900_phase14_orbit_family_comparison.json"
md_path = OUT_MD / "p900_phase14_orbit_family_comparison.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 14 Orbit Family Comparison")
lines.append("")
lines.append("Status: sandbox audit")
lines.append("")
lines.append("Warning: this compares representative split laws from the two preferred orbit families. It does not prove a final P900 law.")
lines.append("")
lines.append("## Families")
lines.append("")
for name, s in families.items():
    lines.append(f"- {name}: {s}")
lines.append("")
lines.append("## Total comparison")
lines.append("")
lines.append(f"- cycle count: {summary['cycle_count']}")
lines.append(f"- same total profile: {same_total_profile}")
lines.append(f"- same length profile: {same_length_profile}")
lines.append("")
for name, p in profiles.items():
    lines.append(f"### {name}")
    lines.append("")
    lines.append(f"- half-turn set: {p['half_turn_set']}")
    lines.append(f"- edge label counts: {p['edge_label_counts']}")
    lines.append(f"- identity closures: {p['identity_closure_count']}")
    lines.append(f"- half-turn closures: {p['half_turn_closure_count']}")
    lines.append(f"- orientation drift: {p['orientation_drift_count']}")
    lines.append(f"- balance gap: {p['identity_half_turn_balance_gap']}")
    lines.append(f"- length closure histogram: {p['length_closure_histogram']}")
    lines.append("")
lines.append("## Length-by-length comparison")
lines.append("")
for length, row in diff_by_length.items():
    lines.append(f"- length {length}: {row}")
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("cycle_count=" + str(summary["cycle_count"]))
print("same_total_profile=" + str(same_total_profile))
print("same_length_profile=" + str(same_length_profile))
for name, p in profiles.items():
    print(name + " identity=" + str(p["identity_closure_count"]) + " half_turn=" + str(p["half_turn_closure_count"]) + " drift=" + str(p["orientation_drift_count"]) + " gap=" + str(p["identity_half_turn_balance_gap"]) + " length_profile=" + str(p["length_closure_histogram"]))
