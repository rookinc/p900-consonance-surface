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
g60_local_states = list(range(60))

g15_edges = []
for i, e1 in enumerate(petersen_edges):
    a, b = e1
    for j in range(i + 1, len(petersen_edges)):
        c, d = petersen_edges[j]
        if len({a, b, c, d}) < 4:
            g15_edges.append((i, j))

# Phase 5 baseline:
# Every G15 edge gets either identity shift 0 or half-turn shift 30.
# We use a deterministic parity labeling by edge index.
edge_shift_undirected = {}
edge_label_undirected = {}
for k, edge in enumerate(g15_edges):
    if k % 2 == 0:
        label = "identity"
        shift = 0
    else:
        label = "half_turn"
        shift = 30
    edge_shift_undirected[edge] = shift
    edge_label_undirected[edge] = label

# Since 30 = -30 mod 60, reverse orientation has the same shift for half-turn.
edge_shift = {}
edge_label = {}
for a, b in g15_edges:
    shift = edge_shift_undirected[(a, b)]
    label = edge_label_undirected[(a, b)]
    edge_shift[(a, b)] = shift
    edge_shift[(b, a)] = shift
    edge_label[(a, b)] = label
    edge_label[(b, a)] = label

# Coupling degree audit.
coupling_edges = []
degree = Counter()
for s, t in g15_edges:
    shift = edge_shift[(s, t)]
    for x in g60_local_states:
        y = (x + shift) % 60
        a = (s, x)
        b = (t, y)
        coupling_edges.append((a, b))
        degree[a] += 1
        degree[b] += 1

degree_values = sorted(degree.values())
degree_histogram = dict(sorted(Counter(degree_values).items()))

# Cycle audit.
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

records = []
holonomy_counter = Counter()
length_counter = Counter()
closure_counter = Counter()

for cyc in cycles:
    shift_sum = 0
    labels = []
    for i in range(len(cyc)):
        a = cyc[i]
        b = cyc[(i + 1) % len(cyc)]
        shift_sum = (shift_sum + edge_shift[(a, b)]) % 60
        labels.append(edge_label[(a, b)])

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
    })

summary = {
    "name": "P900 Phase 5 Binary Half-Turn Holonomy",
    "status": "sandbox_hypothesis",
    "warning": "This is a binary 0/30 baseline, not a proven P900 law.",
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "p900_state_count": 15 * 60,
    "coupling_edge_count": len(coupling_edges),
    "external_degree_min": min(degree_values),
    "external_degree_max": max(degree_values),
    "external_degree_histogram": degree_histogram,
    "cycle_search_max_length": 8,
    "cycle_count": len(records),
    "cycle_length_histogram": dict(sorted(length_counter.items())),
    "holonomy_shift_histogram_mod_60": dict(sorted(holonomy_counter.items())),
    "closure_type_histogram": dict(sorted(closure_counter.items())),
    "identity_closure_count": closure_counter["identity_closure"],
    "half_turn_closure_count": closure_counter["half_turn_closure"],
    "orientation_drift_count": closure_counter["orientation_drift"],
    "first_read": [
        "The binary 0/30 interface preserves uniform external degree 4.",
        "All audited cycles close as either identity or half-turn.",
        "This eliminates orientation drift by restricting local shifts to the G30-style sign grammar.",
        "This is a clean baseline for the 360/180/360 intuition."
    ],
    "records": records,
}

json_path = OUT_JSON / "p900_phase5_binary_half_turn_holonomy.json"
md_path = OUT_MD / "p900_phase5_binary_half_turn_holonomy.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 5 Binary Half-Turn Holonomy")
lines.append("")
lines.append("Status: sandbox hypothesis")
lines.append("")
lines.append("Warning: this is a binary 0/30 baseline, not a proven P900 law.")
lines.append("")
lines.append("## Purpose")
lines.append("")
lines.append("Phase 5 tests a G30-style sign grammar where each G15 edge carries either identity shift 0 or half-turn shift 30.")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- G15 positions: {summary['g15_positions']}")
lines.append(f"- G15 edges: {summary['g15_edges']}")
lines.append(f"- P900 states: {summary['p900_state_count']}")
lines.append(f"- coupling edges: {summary['coupling_edge_count']}")
lines.append(f"- external degree min: {summary['external_degree_min']}")
lines.append(f"- external degree max: {summary['external_degree_max']}")
lines.append(f"- external degree histogram: {summary['external_degree_histogram']}")
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
print("coupling_edge_count=" + str(summary["coupling_edge_count"]))
print("external_degree_histogram=" + str(summary["external_degree_histogram"]))
print("cycle_count=" + str(summary["cycle_count"]))
print("holonomy_shift_histogram_mod_60=" + str(summary["holonomy_shift_histogram_mod_60"]))
print("closure_type_histogram=" + str(summary["closure_type_histogram"]))
