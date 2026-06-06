from pathlib import Path
import json
from collections import Counter, defaultdict, deque

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

phase17 = json.loads((OUT_JSON / "p900_phase17_external_edge_list.json").read_text(encoding="utf-8"))

vertices = [(s, x) for s in range(15) for x in range(60)]
adj = {v: [] for v in vertices}

for rec in phase17["external_edges"]:
    a = tuple(rec["a"])
    b = tuple(rec["b"])
    adj[a].append(b)
    adj[b].append(a)

seen = set()
components = []

for v in vertices:
    if v in seen:
        continue

    q = deque([v])
    seen.add(v)
    members = []

    while q:
        cur = q.popleft()
        members.append(cur)
        for nxt in adj[cur]:
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)

    components.append(sorted(members))

components = sorted(components, key=lambda comp: (min(x for s, x in comp), min(s for s, x in comp)))

component_records = []

for idx, comp in enumerate(components):
    sector_counts = Counter(s for s, x in comp)
    local_values = sorted(x for s, x in comp)
    local_residues_mod_30 = sorted(set(x % 30 for s, x in comp))
    local_parity_counts = Counter(x % 2 for s, x in comp)

    component_records.append({
        "component_index": idx,
        "size": len(comp),
        "sector_count_histogram": dict(sorted(Counter(sector_counts.values()).items())),
        "sectors_present": sorted(sector_counts.keys()),
        "local_min": min(local_values),
        "local_max": max(local_values),
        "local_values": local_values,
        "local_residues_mod_30": local_residues_mod_30,
        "local_residue_mod_30_count": len(local_residues_mod_30),
        "local_parity_counts": dict(sorted(local_parity_counts.items())),
        "members": [[s, x] for s, x in comp],
    })

component_size_histogram = dict(sorted(Counter(len(c) for c in components).items()))
sector_count_patterns = Counter(
    tuple(sorted(rec["sector_count_histogram"].items()))
    for rec in component_records
)
residue_count_histogram = dict(sorted(Counter(rec["local_residue_mod_30_count"] for rec in component_records).items()))

all_components_size_30 = component_size_histogram == {30: 30}
all_components_have_15_sectors = all(len(rec["sectors_present"]) == 15 for rec in component_records)
all_components_two_per_sector = all(rec["sector_count_histogram"] == {2: 15} for rec in component_records)
all_components_single_mod30_residue = all(rec["local_residue_mod_30_count"] == 1 for rec in component_records)

summary = {
    "name": "P900 Phase 18 Component Structure Audit",
    "status": "external_surface_audit",
    "warning": "This audits the external inter-thalion surface only. It does not include internal G60 edges.",
    "source": "p900_phase17_external_edge_list.json",
    "component_count": len(components),
    "component_size_histogram": component_size_histogram,
    "sector_count_pattern_histogram": {str(k): v for k, v in sorted(sector_count_patterns.items(), key=lambda item: str(item[0]))},
    "local_residue_mod_30_count_histogram": residue_count_histogram,
    "all_components_size_30": all_components_size_30,
    "all_components_have_15_sectors": all_components_have_15_sectors,
    "all_components_two_per_sector": all_components_two_per_sector,
    "all_components_single_mod30_residue": all_components_single_mod30_residue,
    "first_read": [
        "The external-only P900 surface decomposes into 30 equal components.",
        "Each component should be checked for sector coverage and local-index organization.",
        "If each component has all 15 sectors with two local states per sector, it is a doubled G15-like sheet.",
        "If each component is organized by one residue mod 30, the external surface is explicitly G30-indexed."
    ],
    "component_records": component_records,
}

json_path = OUT_JSON / "p900_phase18_component_structure.json"
md_path = OUT_MD / "p900_phase18_component_structure.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 18 Component Structure Audit")
lines.append("")
lines.append("Status: external surface audit")
lines.append("")
lines.append("Warning: this audits the external inter-thalion surface only. It does not include internal G60 edges.")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- component count: {summary['component_count']}")
lines.append(f"- component size histogram: {summary['component_size_histogram']}")
lines.append(f"- local residue mod 30 count histogram: {summary['local_residue_mod_30_count_histogram']}")
lines.append(f"- all components size 30: {summary['all_components_size_30']}")
lines.append(f"- all components have 15 sectors: {summary['all_components_have_15_sectors']}")
lines.append(f"- all components have two states per sector: {summary['all_components_two_per_sector']}")
lines.append(f"- all components single mod 30 residue: {summary['all_components_single_mod30_residue']}")
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## First 10 components")
lines.append("")
for rec in component_records[:10]:
    lines.append(f"### Component {rec['component_index']}")
    lines.append("")
    lines.append(f"- size: {rec['size']}")
    lines.append(f"- sectors present: {rec['sectors_present']}")
    lines.append(f"- sector count histogram: {rec['sector_count_histogram']}")
    lines.append(f"- local residues mod 30: {rec['local_residues_mod_30']}")
    lines.append(f"- local values: {rec['local_values']}")
    lines.append("")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("component_count=" + str(summary["component_count"]))
print("component_size_histogram=" + str(summary["component_size_histogram"]))
print("all_components_size_30=" + str(summary["all_components_size_30"]))
print("all_components_have_15_sectors=" + str(summary["all_components_have_15_sectors"]))
print("all_components_two_per_sector=" + str(summary["all_components_two_per_sector"]))
print("all_components_single_mod30_residue=" + str(summary["all_components_single_mod30_residue"]))
print("local_residue_mod_30_count_histogram=" + str(summary["local_residue_mod_30_count_histogram"]))
for rec in component_records[:5]:
    print("component=" + str(rec["component_index"]) + " size=" + str(rec["size"]) + " residues_mod30=" + str(rec["local_residues_mod_30"]) + " sector_count_histogram=" + str(rec["sector_count_histogram"]))
