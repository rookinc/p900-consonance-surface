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

maps = {
    "identity": lambda x: x,
    "half_turn_plus_30": lambda x: (x + 30) % 60,
    "forward_step_plus_1": lambda x: (x + 1) % 60,
    "backward_step_minus_1": lambda x: (x - 1) % 60,
}

variant_summaries = {}

for name, f in maps.items():
    edges = []
    degree = Counter()

    for s, t in g15_edges:
        for x in g60_local_states:
            y = f(x)
            a = (s, x)
            b = (t, y)
            edges.append((a, b))
            degree[a] += 1
            degree[b] += 1

    degree_values = sorted(degree.values())
    variant_summaries[name] = {
        "edge_count": len(edges),
        "external_degree_min": min(degree_values),
        "external_degree_max": max(degree_values),
        "external_degree_histogram": dict(sorted(Counter(degree_values).items())),
    }

all_uniform_degree_4 = all(
    v["external_degree_min"] == 4 and
    v["external_degree_max"] == 4 and
    v["external_degree_histogram"] == {4: 900}
    for v in variant_summaries.values()
)

summary = {
    "name": "P900 Phase 2 Orientation Variant Stubs",
    "status": "sandbox_hypothesis",
    "warning": "These are simple orientation maps, not proven P900 interface laws.",
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "g60_local_states_per_position": len(g60_local_states),
    "p900_state_count": 15 * 60,
    "tested_maps": list(maps.keys()),
    "variant_summaries": variant_summaries,
    "all_variants_uniform_external_degree_4": all_uniform_degree_4,
    "first_read": [
        "The P900 external surface layer remains degree-disciplined under identity, half-turn, and one-step orientation maps.",
        "This suggests the G15 surface grammar is not fragile under simple local orientation shifts.",
        "No internal G60 edges are included yet.",
        "No M or Q interface rule is included yet."
    ],
    "next_tests": [
        "test edge-labeled coupling where each G15 edge chooses a distinct local map",
        "test half-turn maps against the G30 orientation-restoration intuition",
        "add real internal G60 edges when canonical data is available",
        "compare M-guided and Q-guided interface rules against these naive baselines"
    ]
}

json_path = OUT_JSON / "p900_phase2_orientation_variant_stubs.json"
md_path = OUT_MD / "p900_phase2_orientation_variant_stubs.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 2 Orientation Variant Stubs")
lines.append("")
lines.append("Status: sandbox hypothesis")
lines.append("")
lines.append("Warning: these are simple orientation maps, not proven P900 interface laws.")
lines.append("")
lines.append("## Purpose")
lines.append("")
lines.append("Phase 1 tested same-index coupling. Phase 2 tests whether the external P900 surface layer remains disciplined under simple local orientation shifts.")
lines.append("")
lines.append("## Tested maps")
lines.append("")
for name in maps:
    lines.append(f"- {name}")
lines.append("")
lines.append("## Variant summaries")
lines.append("")
for name, data in variant_summaries.items():
    lines.append(f"### {name}")
    lines.append("")
    lines.append(f"- edge count: {data['edge_count']}")
    lines.append(f"- external degree min: {data['external_degree_min']}")
    lines.append(f"- external degree max: {data['external_degree_max']}")
    lines.append(f"- external degree histogram: {data['external_degree_histogram']}")
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
print("tested_maps=" + ",".join(summary["tested_maps"]))
print("all_variants_uniform_external_degree_4=" + str(all_uniform_degree_4))
for name, data in variant_summaries.items():
    print(name + ": edges=" + str(data["edge_count"]) + " degree_min=" + str(data["external_degree_min"]) + " degree_max=" + str(data["external_degree_max"]) + " histogram=" + str(data["external_degree_histogram"]))
