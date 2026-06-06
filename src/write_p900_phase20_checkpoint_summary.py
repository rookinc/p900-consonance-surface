from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

def read_json(name):
    return json.loads((OUT_JSON / name).read_text(encoding="utf-8"))

phase8 = read_json("p900_phase8_candidate_law_verification_packet.json")
phase12 = read_json("p900_phase12_candidate_law_supersession_note.json")
phase13 = read_json("p900_phase13_candidate_orbit_families.json")
phase15 = read_json("p900_phase15_local_balance_score.json")
phase16 = read_json("p900_phase16_preferred_representative_edge_law.json")
phase17 = read_json("p900_phase17_external_edge_list.json")
phase18 = read_json("p900_phase18_component_structure.json")
phase19 = read_json("p900_phase19_doubled_g15_sheet_audit.json")

checks = {
    "address_space_is_900": phase17["p900_vertex_count"] == 900,
    "external_edge_count_is_1800": phase17["external_edge_count"] == 1800,
    "external_degree_uniform_4": phase17["degree_histogram"] == {"4": 900} or phase17["degree_histogram"] == {4: 900},
    "external_layer_not_connected": phase17["connected"] is False,
    "external_component_count_is_30": phase18["component_count"] == 30,
    "components_are_size_30": phase18["all_components_size_30"] is True,
    "components_have_all_15_sectors": phase18["all_components_have_15_sectors"] is True,
    "components_have_two_states_per_sector": phase18["all_components_two_per_sector"] is True,
    "components_are_single_mod30_residue": phase18["all_components_single_mod30_residue"] is True,
    "sheets_are_2_lifts_of_g15": phase19["all_sheets_2_lifts_of_g15"] is True,
    "sheets_are_4_regular": phase19["all_sheets_4_regular"] is True,
    "sheets_have_60_edges": phase19["all_sheets_have_60_edges"] is True,
    "sheets_same_type": phase19["all_sheets_same_type"] is True,
}

checkpoint_ok = all(checks.values())

packet = {
    "name": "P900 Phase 20 Checkpoint Summary",
    "status": "checkpoint_ok" if checkpoint_ok else "needs_review",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "warning": "This summarizes the external P900 sandbox through Phase 19. It is not a theorem and does not include internal G60 edges.",
    "checks": checks,
    "checkpoint_ok": checkpoint_ok,
    "current_claim_ladder": [
        "P900 is currently treated as a candidate consonance surface, not a proven graph identity.",
        "The address space is 15 x 60 = 900 states.",
        "G15 = L(Petersen) supplies the inter-thalion adjacency grammar.",
        "Binary 0/30 sign grammar eliminates orientation drift in the audited cycle holonomy tests.",
        "The first labeled candidate law from Phase 7 was superseded by an orbit-family view in Phases 10-13.",
        "The current preferred representative is gap1_orbit_2 with half-turn set [0,1,2,3,9].",
        "The preferred external edge law produces 1800 inter-thalion edges and uniform external degree 4.",
        "The external-only layer decomposes into 30 components of size 30.",
        "Each component is indexed by one residue mod 30 and contains two states per G15 sector.",
        "Each component is a doubled-G15 sheet, a 2-lift of G15 with 15 cross and 15 parallel lifted edges.",
        "Therefore the preferred external P900 layer is a G30-indexed family of identical doubled-G15 sheets."
    ],
    "key_artifacts": {
        "phase8_verification_packet": "p900_phase8_candidate_law_verification_packet.json",
        "phase12_supersession_note": "p900_phase12_candidate_law_supersession_note.json",
        "phase13_candidate_orbit_families": "p900_phase13_candidate_orbit_families.json",
        "phase15_local_balance_score": "p900_phase15_local_balance_score.json",
        "phase16_preferred_edge_law": "p900_phase16_preferred_representative_edge_law.json",
        "phase17_external_edge_list": "p900_phase17_external_edge_list.json",
        "phase18_component_structure": "p900_phase18_component_structure.json",
        "phase19_doubled_g15_sheet_audit": "p900_phase19_doubled_g15_sheet_audit.json"
    },
    "numeric_summary": {
        "p900_vertices": phase17["p900_vertex_count"],
        "external_edges": phase17["external_edge_count"],
        "external_degree_histogram": phase17["degree_histogram"],
        "component_count": phase18["component_count"],
        "component_size_histogram": phase18["component_size_histogram"],
        "sheet_count": phase19["sheet_count"],
        "sheet_edge_count": 60,
        "sheet_degree_histogram": {"4": 30},
        "preferred_half_turn_set": phase16["preferred_half_turn_set"],
        "preferred_identity_set": phase16["preferred_identity_set"],
        "preferred_family": phase16["preferred_family"],
        "local_balance_score": phase15["preferred_by_local_balance"]["local_balance_score"],
    },
    "do_not_claim_yet": [
        "Do not claim P900 is a fully constructed thalion-cluster graph.",
        "Do not claim the preferred representative is the final P900 law.",
        "Do not claim the external layer alone is connected.",
        "Do not claim internal G60 structure has been added.",
        "Do not identify P900 with AT4val[60,6] or any known graph census object."
    ],
    "next_steps": [
        "write a README checkpoint section",
        "prepare internal G60 import strategy",
        "locate canonical G60/thalean graph edge data",
        "test whether adding internal G60 edges connects the 30 doubled-G15 sheets",
        "compare the preferred representative against the second gap-1 orbit after internal edges are added"
    ]
}

json_path = OUT_JSON / "p900_phase20_checkpoint_summary.json"
md_path = OUT_MD / "p900_phase20_checkpoint_summary.md"

json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 20 Checkpoint Summary")
lines.append("")
lines.append(f"Status: {packet['status']}")
lines.append("")
lines.append("Warning: this summarizes the external P900 sandbox through Phase 19. It is not a theorem and does not include internal G60 edges.")
lines.append("")
lines.append("## Current claim ladder")
lines.append("")
for item in packet["current_claim_ladder"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Checks")
lines.append("")
for k, v in checks.items():
    lines.append(f"- {k}: {v}")
lines.append("")
lines.append(f"checkpoint_ok: {checkpoint_ok}")
lines.append("")
lines.append("## Numeric summary")
lines.append("")
for k, v in packet["numeric_summary"].items():
    lines.append(f"- {k}: {v}")
lines.append("")
lines.append("## Do not claim yet")
lines.append("")
for item in packet["do_not_claim_yet"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Next steps")
lines.append("")
for item in packet["next_steps"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("checkpoint_ok=" + str(checkpoint_ok))
for k, v in checks.items():
    print(k + "=" + str(v))
