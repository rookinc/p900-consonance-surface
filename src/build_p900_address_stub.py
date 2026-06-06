from pathlib import Path
import json

OUT = Path(__file__).resolve().parents[1] / "artifacts" / "json"
OUT.mkdir(parents=True, exist_ok=True)

# Petersen graph with 10 vertices and 15 edges.
# G15 is represented here as L(Petersen), so G15 vertices are Petersen edges.
petersen_edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
]

g15_positions = list(range(15))
g60_states = list(range(60))

# P900 address space.
p900_states = [(s, x) for s in g15_positions for x in g60_states]

# Line graph adjacency on Petersen edges.
g15_edges = []
for i, e1 in enumerate(petersen_edges):
    a, b = e1
    for j in range(i + 1, len(petersen_edges)):
        c, d = petersen_edges[j]
        if len({a, b, c, d}) < 4:
            g15_edges.append((i, j))

summary = {
    "name": "P900 Consonance Surface Stub",
    "status": "sandbox_hypothesis",
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "thalion_states_per_position": len(g60_states),
    "p900_state_count": len(p900_states),
    "address_form": "(g15_position, g60_state)",
    "construction_layers": [
        "address_space_only",
        "internal_g60_edges_later",
        "g15_inter_thalion_adjacency_stubbed",
        "M_or_Q_interface_rule_later"
    ],
    "core_slogan": "P900 is the surface where thalions become vertices without ceasing to be bodies."
}

write_path = OUT / "p900_stub_summary.json"
write_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print("wrote", write_path)
print("g15_positions=" + str(summary["g15_positions"]))
print("g15_edges=" + str(summary["g15_edges"]))
print("thalion_states_per_position=" + str(summary["thalion_states_per_position"]))
print("p900_state_count=" + str(summary["p900_state_count"]))
print("status=" + summary["status"])
