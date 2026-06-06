from pathlib import Path
from collections import Counter, defaultdict
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

G60_PATH = ART_JSON / "p900_phase22_canonical_g60_import.json"
PHASE25 = ART_JSON / "p900_phase25_gap1_orbits_after_g60.json"

OUT_JSON = ART_JSON / "p900_phase29_layer_recoverability.json"
OUT_MD = ART_MD / "p900_phase29_layer_recoverability.md"
OUT_NOTE = NOTES / "phase29_layer_recoverability.md"

PETERSEN_EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
]

CANDIDATES = [
    {
        "name": "gap1_orbit_1_representative",
        "half_turn_set": [0, 1, 2, 3, 5],
    },
    {
        "name": "gap1_orbit_2_representative",
        "half_turn_set": [0, 1, 2, 3, 9],
    },
]

def vid(sector, local):
    return sector * 60 + local

def decode(v):
    return v // 60, v % 60

def pair(a, b):
    return tuple(sorted((a, b)))

def shared_vertex(e1, e2):
    s = set(e1) & set(e2)
    if len(s) != 1:
        raise ValueError("bad Petersen line edge")
    return next(iter(s))

def line_graph_edges():
    rows = []
    for i, e1 in enumerate(PETERSEN_EDGES):
        for j in range(i + 1, len(PETERSEN_EDGES)):
            e2 = PETERSEN_EDGES[j]
            if set(e1) & set(e2):
                rows.append((i, j, shared_vertex(e1, e2)))
    return rows

def build_internal_edges(g60_edges):
    edges = set()
    for sector in range(15):
        for a, b in g60_edges:
            edges.add(pair(vid(sector, a), vid(sector, b)))
    return edges

def build_external_edges(half_turn_set):
    half = set(half_turn_set)
    edges = set()
    edge_law = []
    for i, j, sv in line_graph_edges():
        shift = 30 if sv in half else 0
        label = "half_turn" if shift == 30 else "identity"
        edge_law.append({
            "sector_a": i,
            "sector_b": j,
            "shared_vertex": sv,
            "shift": shift,
            "label": label,
        })
        for x in range(60):
            edges.add(pair(vid(i, x), vid(j, (x + shift) % 60)))
    return edges, edge_law

def classify_edge(a, b):
    sa, la = decode(a)
    sb, lb = decode(b)

    if sa == sb:
        return "internal_same_sector"

    if la == lb:
        return "external_identity_same_local"

    if (lb - la) % 60 == 30 or (la - lb) % 60 == 30:
        return "external_half_turn_mod30"

    return "mixed_or_unexpected"

def audit_candidate(candidate, internal_edges):
    external_edges, edge_law = build_external_edges(candidate["half_turn_set"])
    combined_edges = internal_edges | external_edges

    class_counts = Counter()
    sector_internal_counts = Counter()
    sector_pair_external_counts = Counter()
    residue_external_counts = Counter()
    bad_edges = []

    for a, b in sorted(combined_edges):
        cls = classify_edge(a, b)
        class_counts[cls] += 1

        sa, la = decode(a)
        sb, lb = decode(b)

        if cls == "internal_same_sector":
            sector_internal_counts[sa] += 1
        elif cls in ("external_identity_same_local", "external_half_turn_mod30"):
            sector_pair_external_counts[tuple(sorted((sa, sb)))] += 1
            residue_external_counts[la % 30] += 1
        else:
            if len(bad_edges) < 20:
                bad_edges.append([a, b, [sa, la], [sb, lb]])

    sector_fibers = {}
    for s in range(15):
        verts = [vid(s, x) for x in range(60)]
        sector_fibers[str(s)] = {
            "vertex_count": len(verts),
            "internal_edge_count": sector_internal_counts[s],
        }

    residue_sheets = {}
    for r in range(30):
        verts = [vid(s, r) for s in range(15)] + [vid(s, r + 30) for s in range(15)]
        residue_sheets[str(r)] = {
            "vertex_count": len(verts),
            "external_edge_count": residue_external_counts[r],
        }

    expected_sector_pair_counts = Counter()
    for row in edge_law:
        expected_sector_pair_counts[tuple(sorted((row["sector_a"], row["sector_b"])))] = 60

    checks = {
        "combined_edge_count_is_3600": len(combined_edges) == 3600,
        "internal_edges_are_same_sector": class_counts["internal_same_sector"] == 1800,
        "external_edges_are_shift_0_or_30": (
            class_counts["external_identity_same_local"] + class_counts["external_half_turn_mod30"] == 1800
        ),
        "unexpected_edge_count_is_0": class_counts["mixed_or_unexpected"] == 0,
        "all_sector_fibers_have_60_vertices": all(v["vertex_count"] == 60 for v in sector_fibers.values()),
        "all_sector_fibers_have_120_internal_edges": all(v["internal_edge_count"] == 120 for v in sector_fibers.values()),
        "all_residue_sheets_have_30_vertices": all(v["vertex_count"] == 30 for v in residue_sheets.values()),
        "all_residue_sheets_have_60_external_edges": all(v["external_edge_count"] == 60 for v in residue_sheets.values()),
        "all_g15_sector_pairs_have_60_external_edges": (
            dict(sector_pair_external_counts) == dict(expected_sector_pair_counts)
        ),
    }

    checks["layer_recoverability_ok"] = all(checks.values())

    return {
        "name": candidate["name"],
        "half_turn_set": candidate["half_turn_set"],
        "identity_set": [x for x in range(10) if x not in set(candidate["half_turn_set"])],
        "combined_edge_count": len(combined_edges),
        "edge_class_counts": dict(sorted(class_counts.items())),
        "sector_internal_edge_count_histogram": dict(sorted(Counter(sector_internal_counts.values()).items())),
        "residue_external_edge_count_histogram": dict(sorted(Counter(residue_external_counts.values()).items())),
        "sector_pair_external_edge_count_histogram": dict(sorted(Counter(sector_pair_external_counts.values()).items())),
        "sector_fiber_sample": {k: sector_fibers[k] for k in list(sector_fibers.keys())[:5]},
        "residue_sheet_sample": {k: residue_sheets[k] for k in list(residue_sheets.keys())[:5]},
        "bad_edges_sample": bad_edges,
        "checks": checks,
    }

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, obj):
    lines = []
    lines.append("# P900 Phase 29 Layer Recoverability Audit")
    lines.append("")
    lines.append("Status: " + obj["status"])
    lines.append("")
    lines.append("Warning: " + obj["warning"])
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(obj["purpose"])
    lines.append("")
    lines.append("## Comparison")
    lines.append("")
    for k, v in obj["comparison"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Candidate audits")
    lines.append("")
    for row in obj["candidate_audits"]:
        lines.append("### " + row["name"])
        lines.append("")
        lines.append(f"- half_turn_set: {row['half_turn_set']}")
        lines.append(f"- identity_set: {row['identity_set']}")
        lines.append(f"- combined_edge_count: {row['combined_edge_count']}")
        lines.append(f"- edge_class_counts: {row['edge_class_counts']}")
        lines.append(f"- sector_internal_edge_count_histogram: {row['sector_internal_edge_count_histogram']}")
        lines.append(f"- residue_external_edge_count_histogram: {row['residue_external_edge_count_histogram']}")
        lines.append(f"- sector_pair_external_edge_count_histogram: {row['sector_pair_external_edge_count_histogram']}")
        lines.append("")
        lines.append("Checks:")
        lines.append("")
        for k, v in row["checks"].items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    lines.append("## First read")
    lines.append("")
    for item in obj["first_read"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

g60 = json.loads(G60_PATH.read_text(encoding="utf-8"))
internal_edges = build_internal_edges([tuple(e) for e in g60["g60_edges"]])

audits = [audit_candidate(c, internal_edges) for c in CANDIDATES]

comparison = {
    "both_layer_recoverability_ok": all(a["checks"]["layer_recoverability_ok"] for a in audits),
    "same_edge_class_counts": len({json.dumps(a["edge_class_counts"], sort_keys=True) for a in audits}) == 1,
    "same_sector_internal_histogram": len({json.dumps(a["sector_internal_edge_count_histogram"], sort_keys=True) for a in audits}) == 1,
    "same_residue_external_histogram": len({json.dumps(a["residue_external_edge_count_histogram"], sort_keys=True) for a in audits}) == 1,
    "same_sector_pair_external_histogram": len({json.dumps(a["sector_pair_external_edge_count_histogram"], sort_keys=True) for a in audits}) == 1,
}

status = (
    "layer_recoverability_ok_for_both_gap1_orbits"
    if comparison["both_layer_recoverability_ok"]
    else "layer_recoverability_needs_review"
)

first_read = [
    "Phase 29 checks whether the combined P900 graph still preserves the address-layer grammar.",
    "Internal G60 edges should be exactly the same-sector edges.",
    "External P900 edges should be exactly the inter-sector shift-0 or shift-30 edges.",
    "Each sector fiber should recover one 60-state G60 copy with 120 internal edges.",
    "Each mod-30 residue sheet should recover a 30-vertex doubled-G15 external sheet with 60 external edges.",
]

if comparison["both_layer_recoverability_ok"]:
    first_read.append("Both gap-1 orbit representatives pass the layer recoverability audit.")
else:
    first_read.append("At least one candidate fails a recoverability check.")

obj = {
    "phase": 29,
    "name": "P900 Phase 29 Layer Recoverability Audit",
    "status": status,
    "warning": "This audits recoverability of known address layers. It does not prove canonical uniqueness.",
    "purpose": "Test whether G15 sector fibers, internal G60 copies, and G30 residue sheets remain recoverable after overlay.",
    "source_artifacts": {
        "g60_import": str(G60_PATH),
        "phase25": str(PHASE25),
    },
    "candidate_audits": audits,
    "comparison": comparison,
    "first_read": first_read,
}

write_json(OUT_JSON, obj)
write_md(OUT_MD, obj)
write_md(OUT_NOTE, obj)

print("wrote", OUT_JSON)
print("wrote", OUT_MD)
print("wrote", OUT_NOTE)
print("status=" + status)
for row in audits:
    print(row["name"])
    print("  layer_recoverability_ok=" + str(row["checks"]["layer_recoverability_ok"]))
    print("  edge_class_counts=" + str(row["edge_class_counts"]))
    print("  sector_internal_edge_count_histogram=" + str(row["sector_internal_edge_count_histogram"]))
    print("  residue_external_edge_count_histogram=" + str(row["residue_external_edge_count_histogram"]))
