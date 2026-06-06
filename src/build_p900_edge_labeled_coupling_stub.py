from pathlib import Path
import json
from collections import Counter

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

map_specs = [
    ("identity", 0),
    ("half_turn_plus_30", 30),
    ("forward_step_plus_1", 1),
    ("backward_step_minus_1", -1),
]

edge_labels = {}
label_counts = Counter()
for k, edge in enumerate(g15_edges):
    label_name, shift = map_specs[k % len(map_specs)]
    edge_labels[str(edge)] = {
        "label": label_name,
        "shift_mod_60": shift,
    }
    label_counts[label_name] += 1

coupling_edges = []
degree = Counter()

for k, (s, t) in enumerate(g15_edges):
    label_name, shift = map_specs[k % len(map_specs)]
    for x in g60_local_states:
        y = (x + shift) % 60
        a = (s, x)
        b = (t, y)
        coupling_edges.append((a, b))
        degree[a] += 1
        degree[b] += 1

degree_values = sorted(degree.values())
degree_histogram = dict(sorted(Counter(degree_values).items()))

uniform_external_degree_4 = (
    min(degree_values) == 4 and
    max(degree_values) == 4 and
    degree_histogram == {4: 900}
)

summary = {
    "name": "P900 Phase 3 Edge-Labeled Coupling Stub",
    "status": "sandbox_hypothesis",
    "warning": "This is a deterministic stitched-interface baseline, not a proven P900 law.",
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "g60_local_states_per_position": len(g60_local_states),
    "p900_state_count": 15 * 60,
    "edge_label_pattern": [name for name, shift in map_specs],
    "edge_label_counts": dict(sorted(label_counts.items())),
    "coupling_edge_count": len(coupling_edges),
    "external_degree_min": min(degree_values),
    "external_degree_max": max(degree_values),
    "external_degree_histogram": degree_histogram,
    "uniform_external_degree_4": uniform_external_degree_4,
    "edge_labels": edge_labels,
    "first_read": [
        "The P900 external surface layer remains uniformly degree 4 under a deterministic edge-labeled stitching rule.",
        "This is less product-like than applying one global local map everywhere.",
        "The result suggests that G15 adjacency can host heterogeneous local orientation maps without immediate degree collapse.",
        "No internal G60 edges are included yet.",
        "No M or Q interface rule is included yet."
    ],
    "next_tests": [
        "test cycle holonomy around cycles in G15 under edge-labeled shifts",
        "compare edge-label shift sums against G15 cycle structure",
        "introduce a half-turn-heavy G30-oriented labeling",
        "add internal G60 edges when canonical data is available",
        "compare M-guided and Q-guided interface rules against these baselines"
    ]
}

json_path = OUT_JSON / "p900_phase3_edge_labeled_coupling_stub.json"
md_path = OUT_MD / "p900_phase3_edge_labeled_coupling_stub.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 3 Edge-Labeled Coupling Stub")
lines.append("")
lines.append("Status: sandbox hypothesis")
lines.append("")
lines.append("Warning: this is a deterministic stitched-interface baseline, not a proven P900 law.")
lines.append("")
lines.append("## Purpose")
lines.append("")
lines.append("Phase 3 tests a stitched surface rule where different G15 edges carry different local orientation maps.")
lines.append("")
lines.append("## Edge-label pattern")
lines.append("")
for name, shift in map_specs:
    lines.append(f"- {name}: shift {shift} mod 60")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- G15 positions: {summary['g15_positions']}")
lines.append(f"- G15 edges: {summary['g15_edges']}")
lines.append(f"- local thalion states per position: {summary['g60_local_states_per_position']}")
lines.append(f"- P900 states: {summary['p900_state_count']}")
lines.append(f"- coupling edges: {summary['coupling_edge_count']}")
lines.append(f"- edge label counts: {summary['edge_label_counts']}")
lines.append(f"- external degree min: {summary['external_degree_min']}")
lines.append(f"- external degree max: {summary['external_degree_max']}")
lines.append(f"- external degree histogram: {summary['external_degree_histogram']}")
lines.append(f"- uniform external degree 4: {summary['uniform_external_degree_4']}")
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
print("coupling_edge_count=" + str(summary["coupling_edge_count"]))
print("edge_label_counts=" + str(summary["edge_label_counts"]))
print("external_degree_min=" + str(summary["external_degree_min"]))
print("external_degree_max=" + str(summary["external_degree_max"]))
print("external_degree_histogram=" + str(summary["external_degree_histogram"]))
print("uniform_external_degree_4=" + str(summary["uniform_external_degree_4"]))
