from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"

def read_json(name):
    return json.loads((OUT_JSON / name).read_text(encoding="utf-8"))

phase7 = read_json("p900_phase7_candidate_binary_consonance_law.json")
phase9 = read_json("p900_phase9_candidate_law_relabeling_audit.json")
phase10 = read_json("p900_phase10_vertex_split_families.json")
phase11 = read_json("p900_phase11_vertex_split_orbits.json")

packet = {
    "name": "P900 Phase 12 Candidate Law Supersession Note",
    "status": "supersession_checkpoint",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "warning": "This is an audit-trail note. It does not prove a final P900 law.",
    "superseded_item": {
        "phase": "phase7",
        "name": "shared_vertex_parity_binary_consonance",
        "former_status": "candidate_law_sandbox",
        "new_status": "stable baseline, not preferred final candidate"
    },
    "reason_for_supersession": [
        "Phase 7 promoted the odd/even shared Petersen vertex parity rule because it was incidence-derived and balanced better than earlier simple baselines.",
        "Phase 9 showed the Phase 7 closure profile is constant under all 120 Petersen automorphisms.",
        "Phase 10 showed the Phase 7 split is not optimal among all 252 five-vertex half-turn sets.",
        "Phase 11 showed the best balance gap belongs to two Petersen automorphism orbits of size 60 each."
    ],
    "phase7_profile": {
        "edge_label_counts": phase7["edge_label_counts"],
        "external_degree_histogram": phase7["external_degree_histogram"],
        "phase6_support": phase7["phase6_support"]
    },
    "phase9_profile": {
        "automorphism_count": phase9["automorphism_count"],
        "distinct_profile_count": phase9["distinct_profile_count"],
        "profile_is_constant_under_petersen_automorphisms": phase9["profile_is_constant_under_petersen_automorphisms"],
        "all_profiles_no_orientation_drift": phase9["all_profiles_no_orientation_drift"],
        "best_identity_half_turn_balance_gap": phase9["best_identity_half_turn_balance_gap"],
        "worst_identity_half_turn_balance_gap": phase9["worst_identity_half_turn_balance_gap"]
    },
    "phase10_profile": {
        "tested_half_turn_sets": phase10["tested_half_turn_sets"],
        "best_identity_half_turn_balance_gap": phase10["best_identity_half_turn_balance_gap"],
        "best_profile_count": phase10["best_profile_count"],
        "candidate_rank": phase10["candidate_rank"],
        "candidate_profile": phase10["candidate_profile"],
        "gap_histogram": phase10["gap_histogram"]
    },
    "phase11_profile": {
        "orbit_count": phase11["orbit_count"],
        "candidate_orbit_rank": phase11["candidate_orbit_rank"],
        "best_orbits": phase11["orbits"][:2],
        "previous_candidate_orbit": phase11["orbits"][2] if len(phase11["orbits"]) > 2 else None
    },
    "current_working_position": [
        "P900 remains a candidate consonance surface, not a proven graph identity.",
        "Binary 0/30 sign grammar remains strongly supported as the drift-free surface discipline.",
        "The Phase 7 parity law is retained as a stable baseline.",
        "The preferred next candidate should be selected from the two best gap-1 Petersen split-orbit families found in Phase 11.",
        "Future work should treat the best object as an orbit family, not a single labeled split."
    ],
    "next_steps": [
        "promote the two gap-1 split orbits as candidate consonance families",
        "choose one representative from each best orbit for further testing",
        "compare orbit 1 and orbit 2 against added internal G60 data",
        "avoid claiming the Phase 7 odd/even split as final"
    ]
}

json_path = OUT_JSON / "p900_phase12_candidate_law_supersession_note.json"
md_path = OUT_MD / "p900_phase12_candidate_law_supersession_note.md"

json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 12 Candidate Law Supersession Note")
lines.append("")
lines.append("Status: supersession checkpoint")
lines.append("")
lines.append("Warning: this is an audit-trail note. It does not prove a final P900 law.")
lines.append("")
lines.append("## Superseded item")
lines.append("")
lines.append("- Phase: Phase 7")
lines.append("- Name: `shared_vertex_parity_binary_consonance`")
lines.append("- Former status: candidate law sandbox")
lines.append("- New status: stable baseline, not preferred final candidate")
lines.append("")
lines.append("## Reason for supersession")
lines.append("")
for item in packet["reason_for_supersession"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Current working position")
lines.append("")
for item in packet["current_working_position"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Key numbers")
lines.append("")
lines.append(f"- Phase 9 automorphisms audited: {phase9['automorphism_count']}")
lines.append(f"- Phase 9 distinct profiles: {phase9['distinct_profile_count']}")
lines.append(f"- Phase 9 profile constant: {phase9['profile_is_constant_under_petersen_automorphisms']}")
lines.append(f"- Phase 10 tested half-turn sets: {phase10['tested_half_turn_sets']}")
lines.append(f"- Phase 10 best balance gap: {phase10['best_identity_half_turn_balance_gap']}")
lines.append(f"- Phase 10 best profile count: {phase10['best_profile_count']}")
lines.append(f"- Phase 10 old candidate rank: {phase10['candidate_rank']}")
lines.append(f"- Phase 11 orbit count: {phase11['orbit_count']}")
lines.append(f"- Phase 11 old candidate orbit rank: {phase11['candidate_orbit_rank']}")
lines.append("")
lines.append("## Preferred next direction")
lines.append("")
lines.append("Promote the two Phase 11 gap-1 split orbits as candidate P900 binary consonance families.")
lines.append("")
lines.append("Do not delete the Phase 7 rule. Keep it as the first stable baseline that led to the stronger orbit-family view.")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("superseded=shared_vertex_parity_binary_consonance")
print("new_status=stable_baseline_not_preferred_final_candidate")
print("phase10_best_gap=" + str(phase10["best_identity_half_turn_balance_gap"]))
print("phase10_old_candidate_rank=" + str(phase10["candidate_rank"]))
print("phase11_old_candidate_orbit_rank=" + str(phase11["candidate_orbit_rank"]))
