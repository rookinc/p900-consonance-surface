from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

# Petersen graph with 10 vertices and 15 edges.
# G15 is represented as L(Petersen), so each G15 position is a Petersen edge.
petersen_edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
]

g15_positions = list(range(15))
g60_local_states = list(range(60))

# Build G15 = L(Petersen) adjacency.
g15_edges = []
for i, e1 in enumerate(petersen_edges):
    a, b = e1
    for j in range(i + 1, len(petersen_edges)):
        c, d = petersen_edges[j]
        if len({a, b, c, d}) < 4:
            g15_edges.append((i, j))

# P900 address space.
p900_states = [(s, x) for s in g15_positions for x in g60_local_states]

# Phase 1 naive identity coupling:
# If sector positions s and t are adjacent in G15, couple (s, x) to (t, x)
# for each local thalion state x.
identity_coupling_edges = []
for s, t in g15_edges:
    for x in g60_local_states:
        identity_coupling_edges.append(((s, x), (t, x)))

degree = Counter()
for a, b in identity_coupling_edges:
    degree[a] += 1
    degree[b] += 1

degree_values = sorted(degree.values())
degree_histogram = dict(sorted(Counter(degree_values).items()))

summary = {
    "name": "P900 Phase 1 Identity Coupling Stub",
    "status": "sandbox_hypothesis",
    "warning": "This is a naive same-index interface rule, not a proven P900 law.",
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "g60_local_states_per_position": len(g60_local_states),
    "p900_state_count": len(p900_states),
    "identity_coupling_rule": "for each G15 edge (s,t), couple (s,x) to (t,x) for every local state x",
    "identity_coupling_edge_count": len(identity_coupling_edges),
    "external_degree_min": min(degree_values),
    "external_degree_max": max(degree_values),
    "external_degree_histogram": degree_histogram,
    "first_read": [
        "The naive identity interface gives every P900 state external degree 4.",
        "This matches the 4-regularity of G15 = L(Petersen).",
        "No internal G60 edges are included yet.",
        "No M or Q interface rule is included yet."
    ],
    "next_tests": [
        "add internal G60 edge layer from canonical thalion data",
        "compare identity coupling against M/Q-guided coupling",
        "test whether total degrees remain disciplined",
        "test whether thalion identity is preserved under inter-thalion coupling"
    ]
}

json_path = OUT_JSON / "p900_phase1_identity_coupling_stub.json"
md_path = OUT_MD / "p900_phase1_identity_coupling_stub.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 1 Identity Coupling Stub")
lines.append("")
lines.append("Status: sandbox hypothesis")
lines.append("")
lines.append("Warning: this is a naive same-index interface rule, not a proven P900 law.")
lines.append("")
lines.append("## Rule")
lines.append("")
lines.append("For each G15 edge `(s,t)`, couple `(s,x)` to `(t,x)` for every local thalion state `x`.")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- G15 positions: {summary['g15_positions']}")
lines.append(f"- G15 edges: {summary['g15_edges']}")
lines.append(f"- local thalion states per position: {summary['g60_local_states_per_position']}")
lines.append(f"- P900 states: {summary['p900_state_count']}")
lines.append(f"- identity coupling edges: {summary['identity_coupling_edge_count']}")
lines.append(f"- external degree min: {summary['external_degree_min']}")
lines.append(f"- external degree max: {summary['external_degree_max']}")
lines.append(f"- external degree histogram: {summary['external_degree_histogram']}")
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Next tests")
lines.append("")
for item in summary["next_tests"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("p900_state_count=" + str(summary["p900_state_count"]))
print("identity_coupling_edge_count=" + str(summary["identity_coupling_edge_count"]))
print("external_degree_min=" + str(summary["external_degree_min"]))
print("external_degree_max=" + str(summary["external_degree_max"]))
print("external_degree_histogram=" + str(summary["external_degree_histogram"]))
