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

def petersen_edge_type(k):
    if 0 <= k <= 4:
        return "outer"
    if 5 <= k <= 9:
        return "spoke"
    return "inner"

g15_positions = list(range(15))
g15_edges = []
shared_vertices = {}

for i, e1 in enumerate(petersen_edges):
    a, b = e1
    for j in range(i + 1, len(petersen_edges)):
        c, d = petersen_edges[j]
        shared = sorted(set(e1).intersection(set((c, d))))
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

def make_edge_shifts(rule_name):
    shifts = {}
    labels = {}

    for k, (a, b) in enumerate(g15_edges):
        ta = petersen_edge_type(a)
        tb = petersen_edge_type(b)
        shared = shared_vertices[(a, b)]

        if rule_name == "all_identity":
            shift = 0
            label = "identity"
        elif rule_name == "all_half_turn":
            shift = 30
            label = "half_turn"
        elif rule_name == "alternating_index":
            shift = 0 if k % 2 == 0 else 30
            label = "identity" if shift == 0 else "half_turn"
        elif rule_name == "shared_vertex_odd_half_turn":
            shift = 30 if shared % 2 == 1 else 0
            label = "half_turn" if shift == 30 else "identity"
        elif rule_name == "different_petersen_edge_type_half_turn":
            shift = 30 if ta != tb else 0
            label = "half_turn" if shift == 30 else "identity"
        elif rule_name == "spoke_touch_half_turn":
            shift = 30 if (ta == "spoke" or tb == "spoke") else 0
            label = "half_turn" if shift == 30 else "identity"
        elif rule_name == "outer_touch_half_turn":
            shift = 30 if (ta == "outer" or tb == "outer") else 0
            label = "half_turn" if shift == 30 else "identity"
        elif rule_name == "inner_touch_half_turn":
            shift = 30 if (ta == "inner" or tb == "inner") else 0
            label = "half_turn" if shift == 30 else "identity"
        else:
            raise ValueError(rule_name)

        shifts[(a, b)] = shift
        shifts[(b, a)] = shift
        labels[(a, b)] = label
        labels[(b, a)] = label

    return shifts, labels

rule_names = [
    "all_identity",
    "all_half_turn",
    "alternating_index",
    "shared_vertex_odd_half_turn",
    "different_petersen_edge_type_half_turn",
    "spoke_touch_half_turn",
    "outer_touch_half_turn",
    "inner_touch_half_turn",
]

rule_summaries = {}

for rule_name in rule_names:
    edge_shift, edge_label = make_edge_shifts(rule_name)

    edge_label_counts = Counter()
    for a, b in g15_edges:
        edge_label_counts[edge_label[(a, b)]] += 1

    holonomy_counter = Counter()
    closure_counter = Counter()
    length_closure = defaultdict(Counter)

    for cyc in cycles:
        shift_sum = 0
        for i in range(len(cyc)):
            a = cyc[i]
            b = cyc[(i + 1) % len(cyc)]
            shift_sum = (shift_sum + edge_shift[(a, b)]) % 60

        if shift_sum == 0:
            closure_type = "identity_closure"
        elif shift_sum == 30:
            closure_type = "half_turn_closure"
        else:
            closure_type = "orientation_drift"

        holonomy_counter[shift_sum] += 1
        closure_counter[closure_type] += 1
        length_closure[str(len(cyc))][closure_type] += 1

    identity_count = closure_counter["identity_closure"]
    half_count = closure_counter["half_turn_closure"]
    drift_count = closure_counter["orientation_drift"]
    balance_gap = abs(identity_count - half_count)

    rule_summaries[rule_name] = {
        "edge_label_counts": dict(sorted(edge_label_counts.items())),
        "holonomy_shift_histogram_mod_60": dict(sorted(holonomy_counter.items())),
        "closure_type_histogram": dict(sorted(closure_counter.items())),
        "identity_closure_count": identity_count,
        "half_turn_closure_count": half_count,
        "orientation_drift_count": drift_count,
        "identity_half_turn_balance_gap": balance_gap,
        "length_closure_histogram": {
            k: dict(sorted(v.items()))
            for k, v in sorted(length_closure.items(), key=lambda item: int(item[0]))
        },
    }

ranked_by_balance = sorted(
    rule_names,
    key=lambda name: (
        rule_summaries[name]["orientation_drift_count"],
        rule_summaries[name]["identity_half_turn_balance_gap"],
        name,
    ),
)

summary = {
    "name": "P900 Phase 6 Binary Label Family Audit",
    "status": "sandbox_hypothesis",
    "warning": "This compares binary 0/30 label families, not proven P900 laws.",
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "cycle_search_max_length": 8,
    "cycle_count": len(cycles),
    "tested_rules": rule_names,
    "rule_summaries": rule_summaries,
    "ranked_by_no_drift_then_balance": ranked_by_balance,
    "first_read": [
        "All binary 0/30 label families eliminate orientation drift by construction.",
        "The useful discriminator is the identity/half-turn closure balance over G15 cycles.",
        "Rules with a smaller balance gap distribute identity and half-turn closures more evenly.",
        "This gives a way to search for a consonance labeling before introducing M or Q."
    ],
}

json_path = OUT_JSON / "p900_phase6_binary_label_families.json"
md_path = OUT_MD / "p900_phase6_binary_label_families.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 6 Binary Label Family Audit")
lines.append("")
lines.append("Status: sandbox hypothesis")
lines.append("")
lines.append("Warning: this compares binary 0/30 label families, not proven P900 laws.")
lines.append("")
lines.append("## Purpose")
lines.append("")
lines.append("Phase 6 compares several binary G30-style edge-label rules on G15.")
lines.append("")
lines.append("Since binary 0/30 labels eliminate orientation drift by construction, the discriminator is identity/half-turn closure balance.")
lines.append("")
lines.append("## Ranking")
lines.append("")
for name in ranked_by_balance:
    data = rule_summaries[name]
    lines.append(f"- {name}: drift {data['orientation_drift_count']}, identity {data['identity_closure_count']}, half-turn {data['half_turn_closure_count']}, balance gap {data['identity_half_turn_balance_gap']}, edge labels {data['edge_label_counts']}")
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
print("ranked_by_no_drift_then_balance:")
for name in ranked_by_balance:
    data = rule_summaries[name]
    print(name + ": drift=" + str(data["orientation_drift_count"]) + " identity=" + str(data["identity_closure_count"]) + " half_turn=" + str(data["half_turn_closure_count"]) + " balance_gap=" + str(data["identity_half_turn_balance_gap"]) + " edge_labels=" + str(data["edge_label_counts"]))
