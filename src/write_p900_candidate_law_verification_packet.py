from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

def read_json(name):
    path = OUT_JSON / name
    return json.loads(path.read_text(encoding="utf-8"))

phase_files = {
    "phase1": "p900_phase1_identity_coupling_stub.json",
    "phase2": "p900_phase2_orientation_variant_stubs.json",
    "phase3": "p900_phase3_edge_labeled_coupling_stub.json",
    "phase4": "p900_phase4_cycle_holonomy_stub.json",
    "phase5": "p900_phase5_binary_half_turn_holonomy.json",
    "phase6": "p900_phase6_binary_label_families.json",
    "phase7": "p900_phase7_candidate_binary_consonance_law.json",
}

phases = {k: read_json(v) for k, v in phase_files.items()}

checks = {
    "p900_state_count_is_900": phases["phase7"]["p900_state_count"] == 900,
    "candidate_edge_labels_balanced_15_15": phases["phase7"]["edge_label_counts"] == {"half_turn": 15, "identity": 15},
    "candidate_external_degree_uniform_4": phases["phase7"]["external_degree_histogram"] == {"4": 900} or phases["phase7"]["external_degree_histogram"] == {4: 900},
    "phase4_arbitrary_stitching_detected_drift": phases["phase4"]["orientation_drift_count"] > 0,
    "phase5_binary_half_turn_removed_drift": phases["phase5"]["orientation_drift_count"] == 0,
    "phase6_candidate_ranked_first": phases["phase6"]["ranked_by_no_drift_then_balance"][0] == "shared_vertex_odd_half_turn",
    "phase6_candidate_balance_gap_7": phases["phase6"]["rule_summaries"]["shared_vertex_odd_half_turn"]["identity_half_turn_balance_gap"] == 7,
    "phase7_candidate_law_named": phases["phase7"]["candidate_law"]["name"] == "shared_vertex_parity_binary_consonance",
}

verification_ok = all(checks.values())

packet = {
    "name": "P900 Candidate Law Verification Packet",
    "status": "verified_sandbox_checkpoint" if verification_ok else "needs_review",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "warning": "This verifies an internal sandbox checkpoint, not a theorem and not a final P900 construction.",
    "candidate_law": phases["phase7"]["candidate_law"],
    "checks": checks,
    "verification_ok": verification_ok,
    "phase_summary": {
        "phase1": {
            "claim": "same-index G15 coupling gives uniform external degree",
            "external_degree_histogram": phases["phase1"]["external_degree_histogram"],
            "coupling_edges": phases["phase1"]["identity_coupling_edge_count"],
        },
        "phase2": {
            "claim": "simple global orientation maps preserve uniform external degree",
            "all_variants_uniform_external_degree_4": phases["phase2"]["all_variants_uniform_external_degree_4"],
            "tested_maps": phases["phase2"]["tested_maps"],
        },
        "phase3": {
            "claim": "heterogeneous edge-labeled stitching preserves uniform external degree",
            "uniform_external_degree_4": phases["phase3"]["uniform_external_degree_4"],
            "edge_label_counts": phases["phase3"]["edge_label_counts"],
        },
        "phase4": {
            "claim": "arbitrary stitched shifts produce orientation drift",
            "closure_type_histogram": phases["phase4"]["closure_type_histogram"],
        },
        "phase5": {
            "claim": "binary 0/30 sign grammar eliminates orientation drift",
            "closure_type_histogram": phases["phase5"]["closure_type_histogram"],
            "holonomy_shift_histogram_mod_60": phases["phase5"]["holonomy_shift_histogram_mod_60"],
        },
        "phase6": {
            "claim": "shared-vertex parity is best among tested binary label families",
            "ranked_by_no_drift_then_balance": phases["phase6"]["ranked_by_no_drift_then_balance"],
            "winner": "shared_vertex_odd_half_turn",
            "winner_summary": phases["phase6"]["rule_summaries"]["shared_vertex_odd_half_turn"],
        },
        "phase7": {
            "claim": "candidate law promoted as shared_vertex_parity_binary_consonance",
            "edge_label_counts": phases["phase7"]["edge_label_counts"],
            "external_degree_histogram": phases["phase7"]["external_degree_histogram"],
            "phase6_support": phases["phase7"]["phase6_support"],
        },
    },
    "working_interpretation": [
        "P900 is currently treated as a candidate consonance surface, not a proven graph identity.",
        "The surface address space is 15 x 60 = 900.",
        "G15 = L(Petersen) supplies the inter-thalion adjacency grammar.",
        "Arbitrary local shifts preserve degree but cause cycle holonomy drift.",
        "Binary 0/30 shifts preserve degree and restrict cycle holonomy to identity or half-turn.",
        "The best tested binary incidence-derived rule assigns identity or half-turn by parity of the shared Petersen vertex.",
    ],
    "next_steps": [
        "add a compact README checkpoint section",
        "add internal G60 data when canonical source files are available",
        "compare the candidate binary law against M-guided and Q-guided interfaces",
        "audit whether candidate law is invariant under relabelings or depends on chosen Petersen labeling",
    ],
}

json_path = OUT_JSON / "p900_phase8_candidate_law_verification_packet.json"
md_path = OUT_MD / "p900_phase8_candidate_law_verification_packet.md"

json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 8 Candidate Law Verification Packet")
lines.append("")
lines.append(f"Status: {packet['status']}")
lines.append("")
lines.append("Warning: this verifies an internal sandbox checkpoint, not a theorem and not a final P900 construction.")
lines.append("")
lines.append("## Candidate law")
lines.append("")
lines.append("Name: `shared_vertex_parity_binary_consonance`")
lines.append("")
lines.append("Rule:")
lines.append("")
lines.append("- shared Petersen vertex even: identity interface, shift 0 mod 60")
lines.append("- shared Petersen vertex odd: half-turn interface, shift 30 mod 60")
lines.append("")
lines.append("## Verification checks")
lines.append("")
for k, v in checks.items():
    lines.append(f"- {k}: {v}")
lines.append("")
lines.append(f"verification_ok: {verification_ok}")
lines.append("")
lines.append("## Phase summary")
lines.append("")
for phase, data in packet["phase_summary"].items():
    lines.append(f"### {phase}")
    lines.append("")
    lines.append(f"- claim: {data['claim']}")
    for kk, vv in data.items():
        if kk != "claim":
            lines.append(f"- {kk}: {vv}")
    lines.append("")
lines.append("## Working interpretation")
lines.append("")
for item in packet["working_interpretation"]:
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
print("verification_ok=" + str(verification_ok))
for k, v in checks.items():
    print(k + "=" + str(v))
