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
shared_vertices = {}

for i, e1 in enumerate(petersen_edges):
    for j in range(i + 1, len(petersen_edges)):
        shared = sorted(set(e1).intersection(set(petersen_edges[j])))
        if shared:
            g15_edges.append((i, j))
            shared_vertices[(i, j)] = shared[0]

edge_law_records = []
edge_label_counts = Counter()
degree = Counter()

for a, b in g15_edges:
    shared = shared_vertices[(a, b)]
    if shared % 2 == 0:
        label = "identity"
        shift = 0
    else:
        label = "half_turn"
        shift = 30

    edge_label_counts[label] += 1
    edge_law_records.append({
        "g15_edge": [a, b],
        "petersen_edge_a": list(petersen_edges[a]),
        "petersen_edge_b": list(petersen_edges[b]),
        "shared_petersen_vertex": shared,
        "shared_vertex_parity": "odd" if shared % 2 else "even",
        "interface_label": label,
        "shift_mod_60": shift,
    })

    for x in g60_local_states:
        y = (x + shift) % 60
        degree[(a, x)] += 1
        degree[(b, y)] += 1

degree_values = sorted(degree.values())
degree_histogram = dict(sorted(Counter(degree_values).items()))

summary = {
    "name": "P900 Phase 7 Candidate Binary Consonance Law",
    "status": "candidate_law_sandbox",
    "warning": "Candidate law only. This is not a theorem and not a final P900 construction.",
    "candidate_law": {
        "name": "shared_vertex_parity_binary_consonance",
        "rule": "For a G15 adjacency arising from two Petersen edges with shared Petersen vertex v, use identity if v is even and half-turn if v is odd.",
        "even_shared_vertex": {
            "interface": "identity",
            "shift_mod_60": 0
        },
        "odd_shared_vertex": {
            "interface": "half_turn",
            "shift_mod_60": 30
        }
    },
    "g15_model": "L(Petersen)",
    "g15_positions": len(g15_positions),
    "g15_edges": len(g15_edges),
    "p900_state_count": 15 * 60,
    "edge_label_counts": dict(sorted(edge_label_counts.items())),
    "external_degree_min": min(degree_values),
    "external_degree_max": max(degree_values),
    "external_degree_histogram": degree_histogram,
    "phase6_support": {
        "cycle_count_audited": 557,
        "identity_closure_count": 282,
        "half_turn_closure_count": 275,
        "orientation_drift_count": 0,
        "identity_half_turn_balance_gap": 7,
        "ranking": "best among tested binary label families by no drift then identity/half-turn balance"
    },
    "interpretation": [
        "This rule is incidence-derived rather than arbitrary index-derived.",
        "The rule uses Petersen shared-vertex parity to assign the inter-thalion interface.",
        "The rule preserves uniform external degree 4.",
        "The rule inherits Phase 6's best observed identity/half-turn cycle balance among tested binary label families.",
        "This is the current preferred baseline for P900 binary consonance."
    ],
    "edge_law_records": edge_law_records
}

json_path = OUT_JSON / "p900_phase7_candidate_binary_consonance_law.json"
md_path = OUT_MD / "p900_phase7_candidate_binary_consonance_law.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 7 Candidate Binary Consonance Law")
lines.append("")
lines.append("Status: candidate law sandbox")
lines.append("")
lines.append("Warning: this is not a theorem and not a final P900 construction.")
lines.append("")
lines.append("## Candidate law")
lines.append("")
lines.append("For a G15 adjacency arising from two Petersen edges with shared Petersen vertex `v`:")
lines.append("")
lines.append("- if `v` is even, use identity interface, shift 0 mod 60")
lines.append("- if `v` is odd, use half-turn interface, shift 30 mod 60")
lines.append("")
lines.append("## Why this rule is preferred")
lines.append("")
lines.append("Phase 6 compared tested binary 0/30 label families. This rule ranked best by no drift first, then identity/half-turn balance.")
lines.append("")
lines.append("Phase 6 support:")
lines.append("")
lines.append("- audited cycles: 557")
lines.append("- identity closures: 282")
lines.append("- half-turn closures: 275")
lines.append("- orientation drift: 0")
lines.append("- balance gap: 7")
lines.append("")
lines.append("## Surface counts")
lines.append("")
lines.append(f"- G15 positions: {summary['g15_positions']}")
lines.append(f"- G15 edges: {summary['g15_edges']}")
lines.append(f"- P900 states: {summary['p900_state_count']}")
lines.append(f"- edge label counts: {summary['edge_label_counts']}")
lines.append(f"- external degree histogram: {summary['external_degree_histogram']}")
lines.append("")
lines.append("## Interpretation")
lines.append("")
for item in summary["interpretation"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Edge law table")
lines.append("")
for rec in edge_law_records:
    lines.append(
        f"- G15 edge {rec['g15_edge']} from Petersen edges "
        f"{rec['petersen_edge_a']} and {rec['petersen_edge_b']}: "
        f"shared vertex {rec['shared_petersen_vertex']} "
        f"({rec['shared_vertex_parity']}), "
        f"{rec['interface_label']} shift {rec['shift_mod_60']} mod 60"
    )
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("candidate_law=shared_vertex_parity_binary_consonance")
print("edge_label_counts=" + str(summary["edge_label_counts"]))
print("external_degree_histogram=" + str(summary["external_degree_histogram"]))
print("phase6_identity_half_turn_balance_gap=7")
print("phase6_orientation_drift_count=0")
