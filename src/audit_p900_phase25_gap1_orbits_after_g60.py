from pathlib import Path
from collections import Counter, deque
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

G60_PATH = ART_JSON / "p900_phase22_canonical_g60_import.json"

OUT_JSON = ART_JSON / "p900_phase25_gap1_orbits_after_g60.json"
OUT_MD = ART_MD / "p900_phase25_gap1_orbits_after_g60.md"
OUT_NOTE = NOTES / "phase25_gap1_orbits_after_g60.md"

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

def pair(a, b):
    return tuple(sorted((a, b)))

def shared_vertex(e1, e2):
    s = set(e1) & set(e2)
    if len(s) != 1:
        raise ValueError(f"edges do not share exactly one vertex: {e1}, {e2}")
    return next(iter(s))

def line_graph_edges():
    rows = []
    for i, e1 in enumerate(PETERSEN_EDGES):
        for j in range(i + 1, len(PETERSEN_EDGES)):
            e2 = PETERSEN_EDGES[j]
            if set(e1) & set(e2):
                rows.append((i, j, shared_vertex(e1, e2)))
    return rows

def build_external_edges(half_turn_set):
    half = set(half_turn_set)
    out = set()
    edge_label_counts = Counter()
    edge_law_table = []

    for i, j, sv in line_graph_edges():
        shift = 30 if sv in half else 0
        label = "half_turn" if shift == 30 else "identity"
        edge_label_counts[label] += 1
        edge_law_table.append({
            "g15_edge": [i, j],
            "petersen_edge_a": list(PETERSEN_EDGES[i]),
            "petersen_edge_b": list(PETERSEN_EDGES[j]),
            "shared_vertex": sv,
            "label": label,
            "shift_mod60": shift,
        })

        for x in range(60):
            out.add(pair(vid(i, x), vid(j, (x + shift) % 60)))

    return out, dict(sorted(edge_label_counts.items())), edge_law_table

def build_internal_edges(g60_edges):
    out = set()
    for sector in range(15):
        for a, b in g60_edges:
            out.add(pair(vid(sector, a), vid(sector, b)))
    return out

def components(vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    seen = set()
    comps = []
    for start in vertices:
        if start in seen:
            continue
        q = deque([start])
        seen.add(start)
        comp = []
        while q:
            v = q.popleft()
            comp.append(v)
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        comps.append(comp)
    return comps

def bfs_distances(root, vertices, adj):
    dist = {root: 0}
    q = deque([root])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)
    return dist

def graph_diameter_and_shell_samples(vertices, edges, sample_roots):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    diameter = 0
    eccentricity_hist = Counter()
    root_shells = {}

    for root in vertices:
        dist = bfs_distances(root, vertices, adj)
        if len(dist) != len(vertices):
            return None, {}, {}
        ecc = max(dist.values())
        diameter = max(diameter, ecc)
        eccentricity_hist[ecc] += 1

        if root in sample_roots:
            shell_hist = Counter(dist.values())
            root_shells[str(root)] = [shell_hist[i] for i in range(ecc + 1)]

    return diameter, dict(sorted(eccentricity_hist.items())), root_shells

def audit_candidate(candidate, internal_edges, g60_edges):
    vertices = list(range(900))
    external_edges, edge_label_counts, edge_law_table = build_external_edges(candidate["half_turn_set"])
    combined_edges = internal_edges | external_edges
    duplicate_edges = internal_edges & external_edges

    degree = Counter()
    for a, b in combined_edges:
        degree[a] += 1
        degree[b] += 1

    comps = components(vertices, combined_edges)
    comp_sizes = [len(c) for c in comps]

    sample_roots = [0, 1, 30, 59, 60, 420, 899]
    diameter, eccentricity_hist, root_shells = graph_diameter_and_shell_samples(
        vertices,
        combined_edges,
        sample_roots,
    )

    return {
        "name": candidate["name"],
        "half_turn_set": candidate["half_turn_set"],
        "identity_set": [x for x in range(10) if x not in set(candidate["half_turn_set"])],
        "edge_label_counts": edge_label_counts,
        "vertex_count": len(vertices),
        "internal_edge_count": len(internal_edges),
        "external_edge_count": len(external_edges),
        "duplicate_edge_count": len(duplicate_edges),
        "combined_edge_count": len(combined_edges),
        "degree_histogram": dict(sorted(Counter(degree[v] for v in vertices).items())),
        "component_count": len(comps),
        "component_size_histogram": dict(sorted(Counter(comp_sizes).items())),
        "connected": len(comps) == 1,
        "diameter_if_connected": diameter,
        "eccentricity_histogram": eccentricity_hist,
        "sample_root_shell_profiles": root_shells,
        "edge_law_table_first_10": edge_law_table[:10],
    }

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, obj):
    lines = []
    lines.append("# P900 Phase 25 Gap-1 Orbits After G60")
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
        for key in [
            "half_turn_set",
            "identity_set",
            "edge_label_counts",
            "vertex_count",
            "internal_edge_count",
            "external_edge_count",
            "duplicate_edge_count",
            "combined_edge_count",
            "degree_histogram",
            "component_count",
            "component_size_histogram",
            "connected",
            "diameter_if_connected",
            "eccentricity_histogram",
            "sample_root_shell_profiles",
        ]:
            lines.append(f"- {key}: {row[key]}")
        lines.append("")
    lines.append("## First read")
    lines.append("")
    for item in obj["first_read"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

g60 = json.loads(G60_PATH.read_text())
g60_edges = [tuple(e) for e in g60["g60_edges"]]
internal_edges = build_internal_edges(g60_edges)

audits = [audit_candidate(c, internal_edges, g60_edges) for c in CANDIDATES]

comparison = {
    "both_connected": all(a["connected"] for a in audits),
    "same_degree_histogram": len({json.dumps(a["degree_histogram"], sort_keys=True) for a in audits}) == 1,
    "same_combined_edge_count": len({a["combined_edge_count"] for a in audits}) == 1,
    "same_diameter": len({a["diameter_if_connected"] for a in audits}) == 1,
    "same_eccentricity_histogram": len({json.dumps(a["eccentricity_histogram"], sort_keys=True) for a in audits}) == 1,
    "diameters": {a["name"]: a["diameter_if_connected"] for a in audits},
    "eccentricity_histograms": {a["name"]: a["eccentricity_histogram"] for a in audits},
}

if comparison["both_connected"] and comparison["same_diameter"] and comparison["same_eccentricity_histogram"]:
    status = "gap1_orbits_tied_after_g60_basic_audit"
elif comparison["both_connected"]:
    status = "gap1_orbits_both_close_but_differ_after_g60"
else:
    status = "gap1_orbit_closure_split_detected"

first_read = [
    "Both gap-1 orbit representatives are tested after adding the same 15 internal canonical G60 copies.",
    "This checks whether Phase 24 closure is unique to the preferred representative or generic across the two best external orbit families.",
]

if comparison["both_connected"]:
    first_read.append("Both representatives produce connected combined P900 graphs.")
else:
    first_read.append("At least one representative fails connected closure after G60 import.")

if comparison["same_diameter"] and comparison["same_eccentricity_histogram"]:
    first_read.append("The basic global distance profile does not distinguish the two representatives.")
else:
    first_read.append("The basic global distance profile distinguishes the two representatives.")

obj = {
    "phase": 25,
    "name": "P900 Phase 25 Gap-1 Orbits After G60",
    "status": status,
    "warning": "This is a basic combined-graph comparison. It does not prove uniqueness or finality.",
    "purpose": "Compare the two Phase 13 gap-1 orbit representatives after internal G60 import.",
    "source_artifacts": {
        "g60_import": str(G60_PATH),
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
    print(
        row["name"],
        "connected=" + str(row["connected"]),
        "diameter=" + str(row["diameter_if_connected"]),
        "degree_histogram=" + str(row["degree_histogram"]),
        "eccentricity_histogram=" + str(row["eccentricity_histogram"]),
    )
