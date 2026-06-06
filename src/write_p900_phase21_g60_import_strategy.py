from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

ART_JSON.mkdir(parents=True, exist_ok=True)
ART_MD.mkdir(parents=True, exist_ok=True)
NOTES.mkdir(parents=True, exist_ok=True)

OUT_JSON = ART_JSON / "p900_phase21_g60_internal_import_strategy.json"
OUT_MD = ART_MD / "p900_phase21_g60_internal_import_strategy.md"
OUT_NOTE = NOTES / "phase21_g60_internal_import_strategy.md"

strategy = {
    "phase": 21,
    "name": "P900 Phase 21 G60 Internal Import Strategy",
    "status": "strategy_checkpoint",
    "warning": "This is an integration plan, not an imported G60 graph and not a closure theorem.",
    "current_external_checkpoint": {
        "p900_vertices": 900,
        "external_edges": 1800,
        "external_degree": 4,
        "external_component_count": 30,
        "external_component_size": 30,
        "external_structure": "G30-indexed family of identical doubled-G15 sheets",
        "internal_g60_edges_added": False,
    },
    "intended_internal_import": {
        "address_form": "(g15_sector, g60_state)",
        "rule": "For each G15 sector s, add one canonical G60/thalean graph copy on local states x=0..59.",
        "edge_form": "(s,x)--(s,y) whenever x--y is a canonical G60 edge.",
        "copies": 15,
        "vertices_per_copy": 60,
        "expected_edges_per_copy_if_g60_4_regular": 120,
        "expected_internal_edges_if_g60_4_regular": 1800,
    },
    "first_combined_candidate": {
        "vertices": 900,
        "external_edges": 1800,
        "expected_internal_edges": 1800,
        "expected_total_edges": 3600,
        "expected_degree_if_no_overlap_and_g60_4_regular": 8,
    },
    "required_source_data": [
        "canonical G60 vertex labels 0..59 or a verified label map into 0..59",
        "canonical G60 edge list",
        "source provenance for the G60 edge list",
        "verification that |V|=60 and |E|=120",
        "verification that the imported G60 copy is the intended thalion / AT4val[60,6] object",
    ],
    "audit_ladder": [
        {
            "phase": 22,
            "name": "canonical_g60_edge_import",
            "question": "Can we import and verify canonical G60 edges with stable local labels 0..59?",
            "checks": [
                "vertex_count_is_60",
                "edge_count_is_120",
                "degree_histogram_expected",
                "connected",
                "source_provenance_present",
            ],
        },
        {
            "phase": 23,
            "name": "combined_p900_graph_audit",
            "question": "What is the graph obtained by overlaying 15 internal G60 copies with the preferred external P900 edge law?",
            "checks": [
                "p900_vertex_count_is_900",
                "internal_edge_count_is_1800_if_g60_4_regular",
                "external_edge_count_is_1800",
                "total_edge_count",
                "degree_histogram",
                "duplicate_edge_count",
            ],
        },
        {
            "phase": 24,
            "name": "closure_component_audit",
            "question": "Do internal G60 edges connect the 30 doubled-G15 external sheets into one object?",
            "checks": [
                "component_count",
                "component_size_histogram",
                "connected",
                "diameter_if_connected",
                "sheet_recoverability_after_internal_import",
            ],
        },
        {
            "phase": 25,
            "name": "orbit_family_comparison_after_g60",
            "question": "Does the preferred gap-1 orbit remain preferred after internal G60 edges are added?",
            "checks": [
                "compare_gap1_orbit_1_combined_graph",
                "compare_gap1_orbit_2_combined_graph",
                "degree_and_component_profiles",
                "diameter_profiles",
                "closure_profiles",
            ],
        },
    ],
    "safe_language": [
        "G60 internal import",
        "15 internal thalion copies",
        "combined P900 candidate",
        "closure audit",
        "external scaffold plus internal body",
    ],
    "avoid_language_until_proven": [
        "P900 is closed",
        "P900 is the final graph",
        "900 proves closure",
        "the external scaffold alone is the full organism",
        "the imported object is canonical without provenance",
    ],
    "working_hypothesis": (
        "If canonical G60 edges are added inside each of the 15 G15 sectors, "
        "the 30 external doubled-G15 sheets may be stitched into a connected "
        "900-state body. This is the next closure test."
    ),
}

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, obj):
    lines = []
    lines.append("# " + obj["name"])
    lines.append("")
    lines.append("Status: " + obj["status"])
    lines.append("")
    lines.append("Warning: " + obj["warning"])
    lines.append("")
    lines.append("## Current external checkpoint")
    lines.append("")
    for k, v in obj["current_external_checkpoint"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Intended internal import")
    lines.append("")
    for k, v in obj["intended_internal_import"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## First combined candidate")
    lines.append("")
    for k, v in obj["first_combined_candidate"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Required source data")
    lines.append("")
    for item in obj["required_source_data"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Audit ladder")
    lines.append("")
    for item in obj["audit_ladder"]:
        lines.append(f"### Phase {item['phase']}: {item['name']}")
        lines.append("")
        lines.append("- question: " + item["question"])
        lines.append("- checks:")
        for check in item["checks"]:
            lines.append(f"  - {check}")
        lines.append("")
    lines.append("## Safe language")
    lines.append("")
    for item in obj["safe_language"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Avoid language until proven")
    lines.append("")
    for item in obj["avoid_language_until_proven"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Working hypothesis")
    lines.append("")
    lines.append(obj["working_hypothesis"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

write_json(OUT_JSON, strategy)
write_md(OUT_MD, strategy)
write_md(OUT_NOTE, strategy)

print("wrote", OUT_JSON)
print("wrote", OUT_MD)
print("wrote", OUT_NOTE)
print("phase=21")
print("status=" + strategy["status"])
print("expected_internal_edges_if_g60_4_regular=" + str(strategy["intended_internal_import"]["expected_internal_edges_if_g60_4_regular"]))
print("expected_total_edges=" + str(strategy["first_combined_candidate"]["expected_total_edges"]))
print("next_phase=22_canonical_g60_edge_import")
