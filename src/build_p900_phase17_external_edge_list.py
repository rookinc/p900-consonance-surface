from pathlib import Path
import json
from collections import Counter, deque

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

phase16 = json.loads((OUT_JSON / "p900_phase16_preferred_representative_edge_law.json").read_text(encoding="utf-8"))

g15_edge_shifts = {}
for rec in phase16["edge_records"]:
    a, b = rec["g15_edge"]
    shift = rec["shift_mod_60"]
    g15_edge_shifts[(a, b)] = shift
    g15_edge_shifts[(b, a)] = shift

p900_vertices = [(s, x) for s in range(15) for x in range(60)]

# Build undirected external edge list using the preferred representative law.
external_edges = []
for rec in phase16["edge_records"]:
    s, t = rec["g15_edge"]
    shift = rec["shift_mod_60"]

    for x in range(60):
        y = (x + shift) % 60
        a = (s, x)
        b = (t, y)
        external_edges.append((a, b))

degree = Counter()
adj = {v: [] for v in p900_vertices}

for a, b in external_edges:
    degree[a] += 1
    degree[b] += 1
    adj[a].append(b)
    adj[b].append(a)

degree_histogram = dict(sorted(Counter(degree.values()).items()))

# Connected components.
seen = set()
component_sizes = []

for v in p900_vertices:
    if v in seen:
        continue
    q = deque([v])
    seen.add(v)
    size = 0

    while q:
        cur = q.popleft()
        size += 1
        for nxt in adj[cur]:
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)

    component_sizes.append(size)

component_sizes = sorted(component_sizes, reverse=True)

# Serialize a compact edge list with list coordinates.
edge_records = [
    {
        "a": [a[0], a[1]],
        "b": [b[0], b[1]]
    }
    for a, b in external_edges
]

summary = {
    "name": "P900 Phase 17 External Edge List",
    "status": "external_surface_checkpoint",
    "warning": "This is the external inter-thalion surface only. It does not include internal G60 edges.",
    "source": "p900_phase16_preferred_representative_edge_law.json",
    "preferred_family": phase16["preferred_family"],
    "preferred_half_turn_set": phase16["preferred_half_turn_set"],
    "p900_vertex_count": len(p900_vertices),
    "external_edge_count": len(external_edges),
    "degree_histogram": degree_histogram,
    "component_count": len(component_sizes),
    "component_sizes": component_sizes,
    "connected": len(component_sizes) == 1,
    "first_read": [
        "The preferred representative external law materializes as 1800 inter-thalion edges.",
        "Each P900 state has external degree 4.",
        "This graph is the external surface layer only.",
        "Internal G60 edges are not included yet."
    ],
    "external_edges": edge_records
}

json_path = OUT_JSON / "p900_phase17_external_edge_list.json"
md_path = OUT_MD / "p900_phase17_external_edge_list.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 17 External Edge List")
lines.append("")
lines.append("Status: external surface checkpoint")
lines.append("")
lines.append("Warning: this is the external inter-thalion surface only. It does not include internal G60 edges.")
lines.append("")
lines.append("## Source")
lines.append("")
lines.append("- source: `p900_phase16_preferred_representative_edge_law.json`")
lines.append(f"- preferred family: {summary['preferred_family']}")
lines.append(f"- preferred half-turn set: {summary['preferred_half_turn_set']}")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- P900 vertices: {summary['p900_vertex_count']}")
lines.append(f"- external edges: {summary['external_edge_count']}")
lines.append(f"- degree histogram: {summary['degree_histogram']}")
lines.append(f"- connected: {summary['connected']}")
lines.append(f"- component count: {summary['component_count']}")
lines.append(f"- component sizes: {summary['component_sizes']}")
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## First 40 edges")
lines.append("")
for rec in edge_records[:40]:
    lines.append(f"- {rec['a']} -- {rec['b']}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("p900_vertex_count=" + str(summary["p900_vertex_count"]))
print("external_edge_count=" + str(summary["external_edge_count"]))
print("degree_histogram=" + str(summary["degree_histogram"]))
print("connected=" + str(summary["connected"]))
print("component_count=" + str(summary["component_count"]))
print("component_sizes=" + str(summary["component_sizes"]))
