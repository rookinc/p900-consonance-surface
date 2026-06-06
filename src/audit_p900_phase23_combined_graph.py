from pathlib import Path
from collections import Counter, deque
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

G60_PATH = ART_JSON / "p900_phase22_canonical_g60_import.json"
EXT_PATH = ART_JSON / "p900_phase17_external_edge_list.json"

OUT_JSON = ART_JSON / "p900_phase23_combined_g60_external_graph.json"
OUT_MD = ART_MD / "p900_phase23_combined_g60_external_graph.md"
OUT_NOTE = NOTES / "phase23_combined_g60_external_graph.md"

def vid(sector, local):
    return sector * 60 + local

def pair(a, b):
    return [a, b] if a < b else [b, a]

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
        comps.append(sorted(comp))
    return comps

def diameter_if_connected(vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    maxd = 0
    for root in vertices:
        dist = {root: 0}
        q = deque([root])
        while q:
            v = q.popleft()
            for w in adj[v]:
                if w not in dist:
                    dist[w] = dist[v] + 1
                    q.append(w)
        if len(dist) != len(vertices):
            return None
        maxd = max(maxd, max(dist.values()))
    return maxd

def local_residue_profile(comp):
    residues = Counter()
    sectors = Counter()
    for v in comp:
        s = v // 60
        x = v % 60
        sectors[s] += 1
        residues[x % 30] += 1
    return {
        "sector_count_histogram": dict(sorted(Counter(sectors.values()).items())),
        "residue_mod30_count": len(residues),
        "residue_mod30_histogram": dict(sorted(Counter(residues.values()).items())),
    }

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, obj):
    lines = []
    lines.append("# P900 Phase 23 Combined G60 + External Graph Audit")
    lines.append("")
    lines.append("Status: " + obj["status"])
    lines.append("")
    lines.append("Warning: " + obj["warning"])
    lines.append("")
    lines.append("## Source artifacts")
    lines.append("")
    for k, v in obj["source_artifacts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    for k, v in obj["counts"].items():
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
    lines.append("## Component summary")
    lines.append("")
    for row in obj["component_summary"][:20]:
        lines.append(
            f"- component {row['index']}: size {row['size']}, "
            f"sectors {row['sector_count_histogram']}, "
            f"residue_mod30_count {row['residue_mod30_count']}, "
            f"residue_mod30_histogram {row['residue_mod30_histogram']}"
        )
    lines.append("")
    lines.append("## Next phase")
    lines.append("")
    lines.append(obj["next_phase"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

g60 = json.loads(G60_PATH.read_text())
ext = json.loads(EXT_PATH.read_text())

vertices = list(range(900))

g60_edges = [tuple(e) for e in g60["g60_edges"]]

internal_edges = []
for sector in range(15):
    for a, b in g60_edges:
        internal_edges.append(pair(vid(sector, a), vid(sector, b)))

external_edges = []
raw_ext_edges = ext.get("external_edges") or ext.get("edge_list") or []
if not raw_ext_edges:
    raise SystemExit("Could not find external edge list in Phase 17 artifact")

for e in raw_ext_edges:
    if isinstance(e, dict):
        a = e["a"]
        b = e["b"]
    else:
        a = e[0]
        b = e[1]
    external_edges.append(pair(vid(int(a[0]), int(a[1])), vid(int(b[0]), int(b[1]))))

internal_set = {tuple(e) for e in internal_edges}
external_set = {tuple(e) for e in external_edges}
combined_set = internal_set | external_set
duplicate_edges = internal_set & external_set
combined_edges = [list(e) for e in sorted(combined_set)]

deg = Counter()
for a, b in combined_edges:
    deg[a] += 1
    deg[b] += 1

degree_hist = Counter(deg[v] for v in vertices)
comps = components(vertices, combined_edges)
comp_sizes = [len(c) for c in comps]
connected = len(comps) == 1
diameter = diameter_if_connected(vertices, combined_edges) if connected else None

component_summary = []
for i, comp in enumerate(comps):
    prof = local_residue_profile(comp)
    component_summary.append({
        "index": i,
        "size": len(comp),
        **prof,
    })

checks = {
    "p900_vertex_count_is_900": len(vertices) == 900,
    "g60_source_import_ok": g60.get("status") == "import_ok",
    "external_edge_count_is_1800": len(external_set) == 1800,
    "internal_edge_count_is_1800": len(internal_set) == 1800,
    "duplicate_edge_count_is_0": len(duplicate_edges) == 0,
    "combined_edge_count_is_3600": len(combined_set) == 3600,
    "degree_regular_8": dict(degree_hist) == {8: 900},
    "connected": connected,
}

status = "combined_graph_connected" if connected else "combined_graph_not_connected"

first_read = [
    "The combined graph overlays 15 internal G60 copies with the preferred Phase 17 external P900 layer.",
    "Internal edges give each state 4 within-sector neighbors.",
    "External edges give each state 4 inter-sector neighbors.",
    "If there is no overlap, the combined candidate should be 8-regular with 3600 edges.",
]

if connected:
    first_read.append("The combined graph is connected; this is the first positive closure-style checkpoint.")
else:
    first_read.append("The combined graph is not connected; closure is not achieved by naive internal G60 overlay alone.")

obj = {
    "phase": 23,
    "name": "P900 Phase 23 Combined G60 + External Graph Audit",
    "status": status,
    "warning": "This audits the first combined graph candidate. It is not yet a final P900 theorem.",
    "source_artifacts": {
        "g60_import": str(G60_PATH),
        "external_edge_list": str(EXT_PATH),
    },
    "counts": {
        "vertex_count": len(vertices),
        "internal_edge_count": len(internal_set),
        "external_edge_count": len(external_set),
        "duplicate_edge_count": len(duplicate_edges),
        "combined_edge_count": len(combined_set),
        "degree_histogram": dict(sorted(degree_hist.items())),
        "component_count": len(comps),
        "component_size_histogram": dict(sorted(Counter(comp_sizes).items())),
        "connected": connected,
        "diameter_if_connected": diameter,
    },
    "checks": checks,
    "component_summary": component_summary,
    "first_read": first_read,
    "next_phase": "Phase 24 should interpret the component/closure result and test whether the second gap-1 orbit changes the combined graph profile.",
}

write_json(OUT_JSON, obj)
write_md(OUT_MD, obj)
write_md(OUT_NOTE, obj)

print("wrote", OUT_JSON)
print("wrote", OUT_MD)
print("wrote", OUT_NOTE)
print("status=" + status)
print("vertex_count=" + str(len(vertices)))
print("internal_edge_count=" + str(len(internal_set)))
print("external_edge_count=" + str(len(external_set)))
print("duplicate_edge_count=" + str(len(duplicate_edges)))
print("combined_edge_count=" + str(len(combined_set)))
print("degree_histogram=" + str(dict(sorted(degree_hist.items()))))
print("component_count=" + str(len(comps)))
print("component_size_histogram=" + str(dict(sorted(Counter(comp_sizes).items()))))
print("connected=" + str(connected))
print("diameter_if_connected=" + str(diameter))
