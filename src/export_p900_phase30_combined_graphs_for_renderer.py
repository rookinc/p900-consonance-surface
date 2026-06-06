from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

G60_PATH = ART_JSON / "p900_phase22_canonical_g60_import.json"
PHASE27 = ART_JSON / "p900_phase27_multi_invariant_selector.json"
PHASE29 = ART_JSON / "p900_phase29_layer_recoverability.json"

OUT_JSON = ART_JSON / "p900_phase30_combined_graph_export.json"
OUT_MD = ART_MD / "p900_phase30_combined_graph_export.md"
OUT_NOTE = NOTES / "phase30_combined_graph_export.md"

PETERSEN_EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
]

CANDIDATES = [
    {
        "id": "gap1_orbit_1",
        "name": "gap1_orbit_1_representative",
        "role": "global-tightness candidate",
        "half_turn_set": [0, 1, 2, 3, 5],
    },
    {
        "id": "gap1_orbit_2",
        "name": "gap1_orbit_2_representative",
        "role": "local-balance provisional selector",
        "half_turn_set": [0, 1, 2, 3, 9],
    },
]

def vid(sector, local):
    return sector * 60 + local

def decode(vertex_id):
    sector = vertex_id // 60
    local = vertex_id % 60
    return {
        "id": vertex_id,
        "sector": sector,
        "local": local,
        "residue_mod30": local % 30,
        "bit": 1 if local >= 30 else 0,
    }

def pair(a, b):
    return tuple(sorted((a, b)))

def shared_vertex(e1, e2):
    s = set(e1) & set(e2)
    if len(s) != 1:
        raise ValueError("bad Petersen line graph edge")
    return next(iter(s))

def line_graph_edges():
    rows = []
    for i, e1 in enumerate(PETERSEN_EDGES):
        for j in range(i + 1, len(PETERSEN_EDGES)):
            e2 = PETERSEN_EDGES[j]
            if set(e1) & set(e2):
                rows.append((i, j, shared_vertex(e1, e2)))
    return rows

def edge_key(a, b):
    x, y = pair(a, b)
    return f"{x}|{y}"

def build_internal_edges(g60_edges):
    edges = {}
    for sector in range(15):
        for a, b in g60_edges:
            va = vid(sector, a)
            vb = vid(sector, b)
            x, y = pair(va, vb)
            edges[edge_key(x, y)] = {
                "source": x,
                "target": y,
                "class": "internal_g60",
                "edge_class": "internal_same_sector",
                "sector_a": sector,
                "sector_b": sector,
                "local_a": a,
                "local_b": b,
                "residue_a": a % 30,
                "residue_b": b % 30,
                "shift_mod60": None,
                "shared_petersen_vertex": None,
            }
    return edges

def build_external_edges(half_turn_set):
    half = set(half_turn_set)
    edges = {}
    edge_law = []

    for i, j, sv in line_graph_edges():
        shift = 30 if sv in half else 0
        label = "half_turn" if shift == 30 else "identity"
        edge_class = "external_half_turn_mod30" if shift == 30 else "external_identity_same_local"

        edge_law.append({
            "sector_a": i,
            "sector_b": j,
            "petersen_edge_a": list(PETERSEN_EDGES[i]),
            "petersen_edge_b": list(PETERSEN_EDGES[j]),
            "shared_petersen_vertex": sv,
            "label": label,
            "shift_mod60": shift,
        })

        for local in range(60):
            va = vid(i, local)
            vb = vid(j, (local + shift) % 60)
            x, y = pair(va, vb)
            dx = decode(x)
            dy = decode(y)
            edges[edge_key(x, y)] = {
                "source": x,
                "target": y,
                "class": "external_p900",
                "edge_class": edge_class,
                "sector_a": dx["sector"],
                "sector_b": dy["sector"],
                "local_a": dx["local"],
                "local_b": dy["local"],
                "residue_a": dx["residue_mod30"],
                "residue_b": dy["residue_mod30"],
                "shift_mod60": shift,
                "shared_petersen_vertex": sv,
            }

    return edges, edge_law

def degree_histogram(edges):
    deg = Counter()
    for e in edges:
        deg[e["source"]] += 1
        deg[e["target"]] += 1
    return dict(sorted(Counter(deg[i] for i in range(900)).items()))

def edge_class_counts(edges):
    return dict(sorted(Counter(e["edge_class"] for e in edges).items()))

def make_candidate_export(candidate, internal_edges):
    external_edges, edge_law = build_external_edges(candidate["half_turn_set"])
    combined = dict(internal_edges)
    overlap = sorted(set(combined) & set(external_edges))
    combined.update(external_edges)

    internal_list = [internal_edges[k] for k in sorted(internal_edges)]
    external_list = [external_edges[k] for k in sorted(external_edges)]
    combined_list = [combined[k] for k in sorted(combined)]

    return {
        "id": candidate["id"],
        "name": candidate["name"],
        "role": candidate["role"],
        "half_turn_set": candidate["half_turn_set"],
        "identity_set": [x for x in range(10) if x not in set(candidate["half_turn_set"])],
        "counts": {
            "vertices": 900,
            "internal_edges": len(internal_list),
            "external_edges": len(external_list),
            "combined_edges": len(combined_list),
            "duplicate_edges": len(overlap),
            "degree_histogram": degree_histogram(combined_list),
            "edge_class_counts": edge_class_counts(combined_list),
        },
        "edge_law_table": edge_law,
        "internal_edges": internal_list,
        "external_edges": external_list,
        "combined_edges": combined_list,
    }

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, obj):
    lines = []
    lines.append("# P900 Phase 30 Combined Graph Export")
    lines.append("")
    lines.append("Status: " + obj["status"])
    lines.append("")
    lines.append("Warning: " + obj["warning"])
    lines.append("")
    lines.append("## Export purpose")
    lines.append("")
    lines.append(obj["purpose"])
    lines.append("")
    lines.append("## Renderer defaults")
    lines.append("")
    for k, v in obj["renderer_defaults"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Candidates")
    lines.append("")
    for c in obj["candidates"]:
        lines.append("### " + c["name"])
        lines.append("")
        lines.append(f"- id: {c['id']}")
        lines.append(f"- role: {c['role']}")
        lines.append(f"- half_turn_set: {c['half_turn_set']}")
        lines.append(f"- identity_set: {c['identity_set']}")
        for k, v in c["counts"].items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in obj["checks"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## First read")
    lines.append("")
    for item in obj["first_read"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

g60 = json.loads(G60_PATH.read_text(encoding="utf-8"))
p27 = json.loads(PHASE27.read_text(encoding="utf-8"))
p29 = json.loads(PHASE29.read_text(encoding="utf-8"))

g60_edges = [tuple(e) for e in g60["g60_edges"]]
internal_edges = build_internal_edges(g60_edges)

vertices = [decode(i) for i in range(900)]
candidate_exports = [make_candidate_export(c, internal_edges) for c in CANDIDATES]

checks = {
    "vertex_count_is_900": len(vertices) == 900,
    "candidate_count_is_2": len(candidate_exports) == 2,
    "all_candidates_have_1800_internal_edges": all(c["counts"]["internal_edges"] == 1800 for c in candidate_exports),
    "all_candidates_have_1800_external_edges": all(c["counts"]["external_edges"] == 1800 for c in candidate_exports),
    "all_candidates_have_3600_combined_edges": all(c["counts"]["combined_edges"] == 3600 for c in candidate_exports),
    "all_candidates_have_no_duplicate_edges": all(c["counts"]["duplicate_edges"] == 0 for c in candidate_exports),
    "all_candidates_are_8_regular": all(c["counts"]["degree_histogram"] == {8: 900} or c["counts"]["degree_histogram"] == {"8": 900} for c in candidate_exports),
    "phase29_layer_recoverability_ok_for_both": p29.get("status") == "layer_recoverability_ok_for_both_gap1_orbits",
}

status = "renderer_export_ok" if all(checks.values()) else "renderer_export_needs_review"

obj = {
    "phase": 30,
    "name": "P900 Phase 30 Combined Graph Export",
    "status": status,
    "warning": "This is a renderer/export artifact. It does not select a final P900 law.",
    "purpose": "Export both closure-bearing combined P900 candidates for Aletheos renderer integration.",
    "source_artifacts": {
        "g60_import": str(G60_PATH),
        "phase27_selector": str(PHASE27),
        "phase29_layer_recoverability": str(PHASE29),
    },
    "renderer_defaults": {
        "default_candidate": p27.get("provisional_selector", "gap1_orbit_2_representative"),
        "default_view": "combined",
        "available_views": [
            "combined",
            "internal_g60",
            "external_p900",
            "residue_sheets",
            "sector_fibers",
        ],
    },
    "vertices": vertices,
    "candidates": candidate_exports,
    "checks": checks,
    "first_read": [
        "Phase 30 exports both closure-bearing P900 candidates.",
        "Orbit 2 remains the provisional selector from Phase 27.",
        "Orbit 1 remains the global-tightness candidate.",
        "Each export preserves internal, external, and combined edge classes for renderer toggles.",
        "The renderer can now show body, surface, and body-plus-surface views without recomputing graph structure.",
    ],
}

write_json(OUT_JSON, obj)
write_md(OUT_MD, obj)
write_md(OUT_NOTE, obj)

print("wrote", OUT_JSON)
print("wrote", OUT_MD)
print("wrote", OUT_NOTE)
print("status=" + status)
print("vertices=" + str(len(vertices)))
for c in candidate_exports:
    print(
        c["name"],
        "internal=" + str(c["counts"]["internal_edges"]),
        "external=" + str(c["counts"]["external_edges"]),
        "combined=" + str(c["counts"]["combined_edges"]),
        "degree_histogram=" + str(c["counts"]["degree_histogram"]),
    )
