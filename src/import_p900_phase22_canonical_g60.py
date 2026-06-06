from pathlib import Path
from collections import Counter, deque
import json

ROOT = Path(__file__).resolve().parents[1]
CORI = ROOT.parents[2]
SRC = CORI / "aletheos.ai" / "public_html" / "json" / "at4val_60_6_3d.json"

ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"
ART_JSON.mkdir(parents=True, exist_ok=True)
ART_MD.mkdir(parents=True, exist_ok=True)
NOTES.mkdir(parents=True, exist_ok=True)

OUT_JSON = ART_JSON / "p900_phase22_canonical_g60_import.json"
OUT_MD = ART_MD / "p900_phase22_canonical_g60_import.md"
OUT_NOTE = NOTES / "phase22_canonical_g60_import.md"

def norm_edge(edge):
    a = int(edge["source"])
    b = int(edge["target"])
    if a == b:
        raise ValueError("loop edge found")
    return [min(a, b), max(a, b)]

def connected(vertices, edges):
    if not vertices:
        return False, []
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    start = vertices[0]
    seen = {start}
    q = deque([start])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                q.append(w)

    return len(seen) == len(vertices), sorted(seen)

def distance_shells_from(root, vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    dist = {root: 0}
    q = deque([root])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)

    hist = Counter(dist.values())
    return [hist[i] for i in range(max(hist) + 1)], max(hist)

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, obj):
    lines = []
    lines.append("# P900 Phase 22 Canonical G60 Import")
    lines.append("")
    lines.append("Status: " + obj["status"])
    lines.append("")
    lines.append("Warning: " + obj["warning"])
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append(f"- source path: {obj['source']['path']}")
    lines.append(f"- source name: {obj['source']['name']}")
    lines.append(f"- source description: {obj['source']['description']}")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in obj["checks"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- vertex count: {obj['counts']['vertex_count']}")
    lines.append(f"- edge count: {obj['counts']['edge_count']}")
    lines.append(f"- degree histogram: {obj['counts']['degree_histogram']}")
    lines.append(f"- connected: {obj['counts']['connected']}")
    lines.append(f"- root 0 shell profile: {obj['counts']['root0_shell_profile']}")
    lines.append(f"- root 0 diameter: {obj['counts']['root0_diameter']}")
    lines.append("")
    lines.append("## Import rule")
    lines.append("")
    lines.append(obj["import_rule"])
    lines.append("")
    lines.append("## First 30 edges")
    lines.append("")
    for e in obj["g60_edges"][:30]:
        lines.append(f"- {e}")
    lines.append("")
    lines.append("## Next phase")
    lines.append("")
    lines.append(obj["next_phase"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

raw = json.loads(SRC.read_text(encoding="utf-8"))

edges = sorted({tuple(norm_edge(e)) for e in raw["edges"]})
edges = [list(e) for e in edges]

node_ids = sorted({int(n["id"]) if isinstance(n, dict) else int(n) for n in raw["nodes"]})
edge_vertices = sorted({x for e in edges for x in e})
all_vertices = sorted(set(node_ids) | set(edge_vertices))

deg = Counter()
for a, b in edges:
    deg[a] += 1
    deg[b] += 1

degree_hist = Counter(deg[v] for v in all_vertices)
is_connected, seen = connected(all_vertices, edges)
shell_profile, diameter = distance_shells_from(0, all_vertices, edges)

checks = {
    "source_exists": SRC.exists(),
    "source_name_is_at4val_60_6": raw.get("name") == "AT4val[60,6]",
    "vertex_count_is_60": len(all_vertices) == 60,
    "edge_count_is_120": len(edges) == 120,
    "vertices_are_0_to_59": all_vertices == list(range(60)),
    "all_edges_are_simple": all(a != b for a, b in edges),
    "all_edges_are_in_range": all(0 <= a < 60 and 0 <= b < 60 for a, b in edges),
    "connected": is_connected,
    "degree_regular_4": dict(degree_hist) == {4: 60},
    "root0_shell_profile_matches_memory": shell_profile == [1, 4, 8, 16, 24, 6, 1],
    "root0_diameter_is_6": diameter == 6,
}

status = "import_ok" if all(checks.values()) else "import_needs_review"

obj = {
    "phase": 22,
    "name": "P900 Phase 22 Canonical G60 Import",
    "status": status,
    "warning": "This imports the local G60 edge list for P900 use. It does not yet build the combined P900 graph.",
    "source": {
        "path": str(SRC),
        "name": raw.get("name"),
        "description": raw.get("description"),
    },
    "checks": checks,
    "counts": {
        "vertex_count": len(all_vertices),
        "edge_count": len(edges),
        "degree_histogram": dict(sorted(degree_hist.items())),
        "connected": is_connected,
        "root0_shell_profile": shell_profile,
        "root0_diameter": diameter,
    },
    "import_rule": "Use these 120 edges as the canonical internal G60/thalean edge list on local states 0..59. In P900, each sector s receives edges (s,a)--(s,b) for every imported G60 edge a--b.",
    "g60_edges": edges,
    "next_phase": "Phase 23 should overlay 15 internal G60 copies with the preferred Phase 17 external P900 edge list and audit the combined 900-state graph.",
}

write_json(OUT_JSON, obj)
write_md(OUT_MD, obj)
write_md(OUT_NOTE, obj)

print("wrote", OUT_JSON)
print("wrote", OUT_MD)
print("wrote", OUT_NOTE)
print("status=" + status)
print("vertex_count=" + str(len(all_vertices)))
print("edge_count=" + str(len(edges)))
print("degree_histogram=" + str(dict(sorted(degree_hist.items()))))
print("connected=" + str(is_connected))
print("root0_shell_profile=" + str(shell_profile))
print("root0_diameter=" + str(diameter))
