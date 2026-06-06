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

# Build G15 = L(Petersen) adjacency.
g15_edges = []
for i, e1 in enumerate(petersen_edges):
    a, b = e1
    for j in range(i + 1, len(petersen_edges)):
        c, d = petersen_edges[j]
        if len({a, b, c, d}) < 4:
            g15_edges.append((i, j))

map_specs = [
    ("identity", 0),
    ("half_turn_plus_30", 30),
    ("forward_step_plus_1", 1),
    ("backward_step_minus_1", -1),
]

# Same deterministic edge labeling used in Phase 3.
edge_shift = {}
edge_label = {}
for k, (a, b) in enumerate(g15_edges):
    name, shift = map_specs[k % len(map_specs)]
    edge_shift[(a, b)] = shift
    edge_shift[(b, a)] = (-shift) % 60
    edge_label[(a, b)] = name
    edge_label[(b, a)] = "reverse_" + name

adj = defaultdict(list)
for a, b in g15_edges:
    adj[a].append(b)
    adj[b].append(a)

for v in adj:
    adj[v] = sorted(adj[v])

def canonical_cycle(cycle):
    # cycle is a list of vertices without repeated endpoint.
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
            elif nxt > -1 and nxt not in path and len(path) < max_len:
                # Small graph, simple DFS is fine.
                dfs(start, nxt, path + [nxt])

    for start in g15_positions:
        dfs(start, start, [start])

    return sorted(found, key=lambda c: (len(c), c))

cycles = simple_cycles_upto(8)

records = []
holonomy_counter = Counter()
length_counter = Counter()
closure_counter = Counter()

for cyc in cycles:
    shift_sum = 0
    labels = []
    steps = []
    for i in range(len(cyc)):
        a = cyc[i]
        b = cyc[(i + 1) % len(cyc)]
        sh = edge_shift[(a, b)]
        shift_sum = (shift_sum + sh) % 60
        labels.append(edge_label[(a, b)])
        steps.append({"from": a, "to": b, "shift_mod_60": sh, "label": edge_label[(a, b)]})

    if shift_sum == 0:
        closure_type = "identity_closure"
    elif shift_sum == 30:
        closure_type = "half_turn_closure"
    else:
        closure_type = "orientation_drift"

    holonomy_counter[shift_sum] += 1
    length_counter[len(cyc)] += 1
    closure_counter[closure_type] += 1

    records.append({
        "cycle": list(cyc),
        "length": len(cyc),
        "shift_sum_mod_60": shift_sum,
        "closure_type": closure_type,
        "labels": labels,
        "steps": steps,
    })

summary = {
    "name": "P900 Phase 4 Cycle Holonomy Stub",
    "status": "sandbox_hypothesis",
    "warning": "This audits the Phase 3 deterministic edge-label baseline, not a proven P900 law.",
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "cycle_search_max_length": 8,
    "cycle_count": len(records),
    "cycle_length_histogram": dict(sorted(length_counter.items())),
    "holonomy_shift_histogram_mod_60": dict(sorted(holonomy_counter.items())),
    "closure_type_histogram": dict(sorted(closure_counter.items())),
    "identity_closure_count": closure_counter["identity_closure"],
    "half_turn_closure_count": closure_counter["half_turn_closure"],
    "orientation_drift_count": closure_counter["orientation_drift"],
    "first_read": [
        "Cycle holonomy measures whether stitched local shifts close consistently around G15 cycles.",
        "0 mod 60 indicates identity closure.",
        "30 mod 60 indicates half-turn closure.",
        "Other residues indicate orientation drift for this baseline labeling.",
        "This is the first audit that speaks directly to G15/G30 orientation-restoration intuition."
    ],
    "records": records,
}

json_path = OUT_JSON / "p900_phase4_cycle_holonomy_stub.json"
md_path = OUT_MD / "p900_phase4_cycle_holonomy_stub.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 4 Cycle Holonomy Stub")
lines.append("")
lines.append("Status: sandbox hypothesis")
lines.append("")
lines.append("Warning: this audits the Phase 3 deterministic edge-label baseline, not a proven P900 law.")
lines.append("")
lines.append("## Purpose")
lines.append("")
lines.append("Phase 4 audits cycle holonomy around G15 cycles under the Phase 3 stitched edge-label rule.")
lines.append("")
lines.append("Interpretation:")
lines.append("")
lines.append("- 0 mod 60 means identity closure.")
lines.append("- 30 mod 60 means half-turn closure.")
lines.append("- any other residue means orientation drift.")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- G15 positions: {summary['g15_positions']}")
lines.append(f"- G15 edges: {summary['g15_edges']}")
lines.append(f"- cycle search max length: {summary['cycle_search_max_length']}")
lines.append(f"- cycle count: {summary['cycle_count']}")
lines.append(f"- cycle length histogram: {summary['cycle_length_histogram']}")
lines.append(f"- holonomy shift histogram mod 60: {summary['holonomy_shift_histogram_mod_60']}")
lines.append(f"- closure type histogram: {summary['closure_type_histogram']}")
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Sample records")
lines.append("")
for rec in records[:20]:
    lines.append(f"- cycle {rec['cycle']} length {rec['length']} shift {rec['shift_sum_mod_60']} closure {rec['closure_type']}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("cycle_count=" + str(summary["cycle_count"]))
print("cycle_length_histogram=" + str(summary["cycle_length_histogram"]))
print("holonomy_shift_histogram_mod_60=" + str(summary["holonomy_shift_histogram_mod_60"]))
print("closure_type_histogram=" + str(summary["closure_type_histogram"]))
