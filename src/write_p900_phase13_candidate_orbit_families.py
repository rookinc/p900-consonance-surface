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

phase11 = read_json("p900_phase11_vertex_split_orbits.json")
phase12 = read_json("p900_phase12_candidate_law_supersession_note.json")

orbits = phase11["orbits"]
best_gap = min(
    orbit["representative_profile"]["identity_half_turn_balance_gap"]
    for orbit in orbits
)

best_orbits = [
    orbit for orbit in orbits
    if orbit["representative_profile"]["identity_half_turn_balance_gap"] == best_gap
]

candidate_families = []
for idx, orbit in enumerate(best_orbits, start=1):
    prof = orbit["representative_profile"]
    candidate_families.append({
        "family_id": "gap1_orbit_" + str(idx),
        "representative_half_turn_set": orbit["representative"],
        "orbit_size": orbit["orbit_size"],
        "identity_closure_count": prof["identity_closure_count"],
        "half_turn_closure_count": prof["half_turn_closure_count"],
        "orientation_drift_count": prof["orientation_drift_count"],
        "identity_half_turn_balance_gap": prof["identity_half_turn_balance_gap"],
        "edge_label_counts": prof["edge_label_counts"],
        "sample_sets": orbit["sample_sets"],
    })

packet = {
    "name": "P900 Phase 13 Candidate Orbit Families",
    "status": "candidate_family_checkpoint",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "warning": "This promotes candidate orbit families, not a final theorem or final P900 construction.",
    "source": {
        "phase11": "p900_phase11_vertex_split_orbits.json",
        "phase12": "p900_phase12_candidate_law_supersession_note.json"
    },
    "selection_rule": "Choose Petersen 5-vertex split orbits with minimal identity/half-turn balance gap among tested 5-of-10 binary half-turn sets.",
    "best_balance_gap": best_gap,
    "candidate_family_count": len(candidate_families),
    "candidate_families": candidate_families,
    "demoted_baseline": phase12["superseded_item"],
    "working_position": [
        "P900 binary consonance is currently best treated as an orbit-family problem.",
        "The preferred candidates are the two Petersen split orbits with balance gap 1.",
        "The old odd/even parity law remains a stable baseline but is no longer preferred.",
        "All candidate families preserve binary 0/30 drift-free closure over the audited G15 cycles.",
        "No internal G60 data has been added yet."
    ],
    "next_tests": [
        "choose one representative from each gap-1 orbit and build explicit edge-law tables",
        "compare orbit 1 and orbit 2 cycle length closure profiles",
        "test whether orbit 1 and orbit 2 are complements or structurally distinct under the audit",
        "add internal G60 data only after the external orbit-family layer is checkpointed"
    ]
}

json_path = OUT_JSON / "p900_phase13_candidate_orbit_families.json"
md_path = OUT_MD / "p900_phase13_candidate_orbit_families.md"

json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 13 Candidate Orbit Families")
lines.append("")
lines.append("Status: candidate family checkpoint")
lines.append("")
lines.append("Warning: this promotes candidate orbit families, not a final theorem or final P900 construction.")
lines.append("")
lines.append("## Selection rule")
lines.append("")
lines.append(packet["selection_rule"])
lines.append("")
lines.append("## Result")
lines.append("")
lines.append(f"- best balance gap: {packet['best_balance_gap']}")
lines.append(f"- candidate family count: {packet['candidate_family_count']}")
lines.append("")
lines.append("## Candidate families")
lines.append("")
for fam in candidate_families:
    lines.append(f"### {fam['family_id']}")
    lines.append("")
    lines.append(f"- representative half-turn set: {fam['representative_half_turn_set']}")
    lines.append(f"- orbit size: {fam['orbit_size']}")
    lines.append(f"- identity closures: {fam['identity_closure_count']}")
    lines.append(f"- half-turn closures: {fam['half_turn_closure_count']}")
    lines.append(f"- orientation drift: {fam['orientation_drift_count']}")
    lines.append(f"- balance gap: {fam['identity_half_turn_balance_gap']}")
    lines.append(f"- edge label counts: {fam['edge_label_counts']}")
    lines.append(f"- sample sets: {fam['sample_sets']}")
    lines.append("")
lines.append("## Working position")
lines.append("")
for item in packet["working_position"]:
    lines.append(f"- {item}")
lines.append("")
lines.append("## Next tests")
lines.append("")
for item in packet["next_tests"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("best_balance_gap=" + str(packet["best_balance_gap"]))
print("candidate_family_count=" + str(packet["candidate_family_count"]))
for fam in candidate_families:
    print(
        fam["family_id"] +
        " representative=" + str(fam["representative_half_turn_set"]) +
        " orbit_size=" + str(fam["orbit_size"]) +
        " identity=" + str(fam["identity_closure_count"]) +
        " half_turn=" + str(fam["half_turn_closure_count"]) +
        " drift=" + str(fam["orientation_drift_count"]) +
        " gap=" + str(fam["identity_half_turn_balance_gap"])
    )
