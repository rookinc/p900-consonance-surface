from pathlib import Path
import json
from datetime import datetime, timezone

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

preferred_half_turn_set = {0, 1, 2, 3, 9}
preferred_identity_set = set(range(10)) - preferred_half_turn_set

g15_edges = []
edge_records = []

for i, e1 in enumerate(petersen_edges):
    for j in range(i + 1, len(petersen_edges)):
        shared = sorted(set(e1).intersection(set(petersen_edges[j])))
        if not shared:
            continue

        shared_vertex = shared[0]
        if shared_vertex in preferred_half_turn_set:
            label = "half_turn"
            shift = 30
        else:
            label = "identity"
            shift = 0

        g15_edges.append((i, j))
        edge_records.append({
            "g15_edge": [i, j],
            "petersen_edge_a": list(e1),
            "petersen_edge_b": list(petersen_edges[j]),
            "shared_petersen_vertex": shared_vertex,
            "interface_label": label,
            "shift_mod_60": shift,
        })

edge_label_counts = {}
for rec in edge_records:
    edge_label_counts[rec["interface_label"]] = edge_label_counts.get(rec["interface_label"], 0) + 1

packet = {
    "name": "P900 Phase 16 Preferred Representative Edge Law",
    "status": "preferred_representative_checkpoint",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "warning": "This is a preferred representative for the next tests, not a final P900 law.",
    "source": {
        "phase13": "p900_phase13_candidate_orbit_families.json",
        "phase15": "p900_phase15_local_balance_score.json"
    },
    "preferred_family": "gap1_orbit_2_representative",
    "preferred_half_turn_set": sorted(preferred_half_turn_set),
    "preferred_identity_set": sorted(preferred_identity_set),
    "rule": "For a G15 adjacency arising from two Petersen edges with shared Petersen vertex v, use half-turn if v is in [0,1,2,3,9], otherwise identity.",
    "g15_edges": len(g15_edges),
    "edge_label_counts": dict(sorted(edge_label_counts.items())),
    "surface_counts": {
        "g15_positions": 15,
        "p900_states": 900,
        "external_degree": 4,
        "inter_thalion_edges": 1800
    },
    "phase15_support": {
        "total_identity_closures": 278,
        "total_half_turn_closures": 279,
        "orientation_drift": 0,
        "total_balance_gap": 1,
        "local_balance_score": 13,
        "max_length_gap": 7,
        "perfectly_balanced_length_count": 3
    },
    "edge_records": edge_records,
    "working_position": [
        "This representative is selected from one of the two best gap-1 Petersen split orbits.",
        "It is preferred over the other tested representative by local balance score.",
        "Both gap-1 orbit families remain alive.",
        "This edge-law table gives a concrete interface rule for subsequent P900 tests."
    ],
    "next_tests": [
        "build explicit P900 external edge list for this representative",
        "audit connectedness and degree distribution of the external-only surface",
        "add a companion edge-law table for the other gap-1 family if needed",
        "prepare for internal G60 edge import"
    ]
}

json_path = OUT_JSON / "p900_phase16_preferred_representative_edge_law.json"
md_path = OUT_MD / "p900_phase16_preferred_representative_edge_law.md"

json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 16 Preferred Representative Edge Law")
lines.append("")
lines.append("Status: preferred representative checkpoint")
lines.append("")
lines.append("Warning: this is a preferred representative for the next tests, not a final P900 law.")
lines.append("")
lines.append("## Preferred representative")
lines.append("")
lines.append("- family: gap1_orbit_2_representative")
lines.append("- half-turn set: [0, 1, 2, 3, 9]")
lines.append("- identity set: [4, 5, 6, 7, 8]")
lines.append("")
lines.append("## Rule")
lines.append("")
lines.append("For a G15 adjacency arising from two Petersen edges with shared Petersen vertex `v`:")
lines.append("")
lines.append("- if `v` is in `[0, 1, 2, 3, 9]`, use half-turn interface, shift 30 mod 60")
lines.append("- otherwise, use identity interface, shift 0 mod 60")
lines.append("")
lines.append("## Support")
lines.append("")
for k, v in packet["phase15_support"].items():
    lines.append(f"- {k}: {v}")
lines.append("")
lines.append("## Surface counts")
lines.append("")
for k, v in packet["surface_counts"].items():
    lines.append(f"- {k}: {v}")
lines.append(f"- edge label counts: {packet['edge_label_counts']}")
lines.append("")
lines.append("## Edge law table")
lines.append("")
for rec in edge_records:
    lines.append(
        f"- G15 edge {rec['g15_edge']} from Petersen edges "
        f"{rec['petersen_edge_a']} and {rec['petersen_edge_b']}: "
        f"shared vertex {rec['shared_petersen_vertex']}, "
        f"{rec['interface_label']} shift {rec['shift_mod_60']} mod 60"
    )
lines.append("")
lines.append("## Working position")
lines.append("")
for item in packet["working_position"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Next tests")
lines.append("")
for item in packet["next_tests"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("preferred_family=" + packet["preferred_family"])
print("preferred_half_turn_set=" + str(packet["preferred_half_turn_set"]))
print("edge_label_counts=" + str(packet["edge_label_counts"]))
print("inter_thalion_edges=1800")
