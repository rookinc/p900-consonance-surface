from pathlib import Path
import json
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

phase16 = json.loads((OUT_JSON / "p900_phase16_preferred_representative_edge_law.json").read_text(encoding="utf-8"))
phase17 = json.loads((OUT_JSON / "p900_phase17_external_edge_list.json").read_text(encoding="utf-8"))
phase18 = json.loads((OUT_JSON / "p900_phase18_component_structure.json").read_text(encoding="utf-8"))

# G15 edges and shifts from preferred Phase 16 law.
g15_edge_records = phase16["edge_records"]
g15_edges = [tuple(rec["g15_edge"]) for rec in g15_edge_records]

# A sheet is indexed by residue r mod 30.
# Its vertices can be represented as (s, bit), where:
#   (s, 0) means P900 state (s, r)
#   (s, 1) means P900 state (s, r + 30)
#
# A shift 0 keeps bit.
# A shift 30 flips bit.
sheet_records = []

for r in range(30):
    sheet_edges = []
    degree = Counter()
    bit_edge_counts = Counter()

    for rec in g15_edge_records:
        s, t = rec["g15_edge"]
        shift = rec["shift_mod_60"]

        if shift == 0:
            pairs = [((s, 0), (t, 0)), ((s, 1), (t, 1))]
            bit_rule = "parallel"
        elif shift == 30:
            pairs = [((s, 0), (t, 1)), ((s, 1), (t, 0))]
            bit_rule = "cross"
        else:
            raise ValueError("unexpected shift " + str(shift))

        bit_edge_counts[bit_rule] += 1

        for a, b in pairs:
            sheet_edges.append((a, b))
            degree[a] += 1
            degree[b] += 1

    degree_histogram = dict(sorted(Counter(degree.values()).items()))
    sheet_records.append({
        "sheet_residue_mod_30": r,
        "vertex_count": 30,
        "edge_count": len(sheet_edges),
        "degree_histogram": degree_histogram,
        "bit_edge_counts": dict(sorted(bit_edge_counts.items())),
        "is_2_lift_of_g15": len(sheet_edges) == 60 and degree_histogram == {4: 30},
        "sample_edges": [
            {
                "a": [a[0], a[1]],
                "b": [b[0], b[1]]
            }
            for a, b in sheet_edges[:20]
        ],
    })

sheet_type_counter = Counter(
    (
        rec["edge_count"],
        tuple(sorted(rec["degree_histogram"].items())),
        tuple(sorted(rec["bit_edge_counts"].items())),
        rec["is_2_lift_of_g15"],
    )
    for rec in sheet_records
)

all_sheets_same_type = len(sheet_type_counter) == 1
all_sheets_2_lifts = all(rec["is_2_lift_of_g15"] for rec in sheet_records)
all_sheets_have_60_edges = all(rec["edge_count"] == 60 for rec in sheet_records)
all_sheets_4_regular = all(rec["degree_histogram"] == {4: 30} for rec in sheet_records)

summary = {
    "name": "P900 Phase 19 Doubled-G15 Sheet Audit",
    "status": "external_surface_audit",
    "warning": "This audits the external inter-thalion surface only. It does not include internal G60 edges.",
    "source": [
        "p900_phase16_preferred_representative_edge_law.json",
        "p900_phase17_external_edge_list.json",
        "p900_phase18_component_structure.json"
    ],
    "sheet_count": len(sheet_records),
    "all_sheets_same_type": all_sheets_same_type,
    "all_sheets_2_lifts_of_g15": all_sheets_2_lifts,
    "all_sheets_have_60_edges": all_sheets_have_60_edges,
    "all_sheets_4_regular": all_sheets_4_regular,
    "sheet_type_histogram": {str(k): v for k, v in sorted(sheet_type_counter.items(), key=lambda item: str(item[0]))},
    "preferred_half_turn_set": phase16["preferred_half_turn_set"],
    "preferred_identity_set": phase16["preferred_identity_set"],
    "first_read": [
        "Each Phase 18 component is a doubled G15 sheet indexed by one residue mod 30.",
        "Within a sheet, shift 0 gives parallel edges between the two bit layers.",
        "Within a sheet, shift 30 gives cross edges between the two bit layers.",
        "The preferred external P900 layer is therefore a G30-indexed family of identical 2-lifts of G15."
    ],
    "sheet_records": sheet_records,
}

json_path = OUT_JSON / "p900_phase19_doubled_g15_sheet_audit.json"
md_path = OUT_MD / "p900_phase19_doubled_g15_sheet_audit.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 19 Doubled-G15 Sheet Audit")
lines.append("")
lines.append("Status: external surface audit")
lines.append("")
lines.append("Warning: this audits the external inter-thalion surface only. It does not include internal G60 edges.")
lines.append("")
lines.append("## Counts")
lines.append("")
lines.append(f"- sheet count: {summary['sheet_count']}")
lines.append(f"- all sheets same type: {summary['all_sheets_same_type']}")
lines.append(f"- all sheets 2-lifts of G15: {summary['all_sheets_2_lifts_of_g15']}")
lines.append(f"- all sheets have 60 edges: {summary['all_sheets_have_60_edges']}")
lines.append(f"- all sheets 4-regular: {summary['all_sheets_4_regular']}")
lines.append(f"- preferred half-turn set: {summary['preferred_half_turn_set']}")
lines.append(f"- preferred identity set: {summary['preferred_identity_set']}")
lines.append("")
lines.append("## Interpretation")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## First 5 sheets")
lines.append("")
for rec in sheet_records[:5]:
    lines.append(f"### Sheet residue {rec['sheet_residue_mod_30']}")
    lines.append("")
    lines.append(f"- vertex count: {rec['vertex_count']}")
    lines.append(f"- edge count: {rec['edge_count']}")
    lines.append(f"- degree histogram: {rec['degree_histogram']}")
    lines.append(f"- bit edge counts: {rec['bit_edge_counts']}")
    lines.append(f"- is 2-lift of G15: {rec['is_2_lift_of_g15']}")
    lines.append("")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("sheet_count=" + str(summary["sheet_count"]))
print("all_sheets_same_type=" + str(summary["all_sheets_same_type"]))
print("all_sheets_2_lifts_of_g15=" + str(summary["all_sheets_2_lifts_of_g15"]))
print("all_sheets_have_60_edges=" + str(summary["all_sheets_have_60_edges"]))
print("all_sheets_4_regular=" + str(summary["all_sheets_4_regular"]))
for rec in sheet_records[:3]:
    print("sheet=" + str(rec["sheet_residue_mod_30"]) + " edges=" + str(rec["edge_count"]) + " degree_histogram=" + str(rec["degree_histogram"]) + " bit_edge_counts=" + str(rec["bit_edge_counts"]) + " is_2_lift=" + str(rec["is_2_lift_of_g15"]))
