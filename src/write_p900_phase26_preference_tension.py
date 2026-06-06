from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

PHASE15 = ART_JSON / "p900_phase15_local_balance_score.json"
PHASE25 = ART_JSON / "p900_phase25_gap1_orbits_after_g60.json"

OUT_JSON = ART_JSON / "p900_phase26_preference_tension_checkpoint.json"
OUT_MD = ART_MD / "p900_phase26_preference_tension_checkpoint.md"
OUT_NOTE = NOTES / "phase26_preference_tension_checkpoint.md"

p15 = json.loads(PHASE15.read_text(encoding="utf-8"))
p25 = json.loads(PHASE25.read_text(encoding="utf-8"))

audits = {row["name"]: row for row in p25["candidate_audits"]}

orbit1 = audits["gap1_orbit_1_representative"]
orbit2 = audits["gap1_orbit_2_representative"]

# Phase 15 selected orbit 2 by local balance score.
phase15_preferred = p15.get("preferred_by_local_balance") or p15.get("preferred_family") or "gap1_orbit_2_representative"

def diameter8_count(row):
    hist = row["eccentricity_histogram"]
    return int(hist.get("8", hist.get(8, 0)))

def ecc6_count(row):
    hist = row["eccentricity_histogram"]
    return int(hist.get("6", hist.get(6, 0)))

orbit1_d8 = diameter8_count(orbit1)
orbit2_d8 = diameter8_count(orbit2)
orbit1_e6 = ecc6_count(orbit1)
orbit2_e6 = ecc6_count(orbit2)

post_g60_tighter = (
    "gap1_orbit_1_representative"
    if orbit1_d8 < orbit2_d8
    else "gap1_orbit_2_representative"
    if orbit2_d8 < orbit1_d8
    else "tie"
)

obj = {
    "phase": 26,
    "name": "P900 Phase 26 Preference Tension Checkpoint",
    "status": "preference_tension_recorded",
    "warning": "This records a selector tension. It does not choose a final P900 law.",
    "inputs": {
        "phase15": str(PHASE15),
        "phase25": str(PHASE25),
    },
    "pre_g60_selector": {
        "selector": "local cycle-length balance score",
        "preferred": phase15_preferred,
        "interpretation": "Orbit 2 was preferred before G60 import because it had the lower local balance score.",
    },
    "post_g60_selector": {
        "selector": "basic global tightness after internal G60 overlay",
        "preferred_by_fewer_diameter8_vertices": post_g60_tighter,
        "orbit1_eccentricity_histogram": orbit1["eccentricity_histogram"],
        "orbit2_eccentricity_histogram": orbit2["eccentricity_histogram"],
        "orbit1_diameter8_vertices": orbit1_d8,
        "orbit2_diameter8_vertices": orbit2_d8,
        "orbit1_eccentricity6_vertices": orbit1_e6,
        "orbit2_eccentricity6_vertices": orbit2_e6,
        "interpretation": "Orbit 1 is globally tighter by this crude distance criterion because it has fewer diameter-8 vertices and more eccentricity-6 vertices.",
    },
    "common_closure_facts": {
        "both_connected": p25["comparison"]["both_connected"],
        "same_degree_histogram": p25["comparison"]["same_degree_histogram"],
        "same_combined_edge_count": p25["comparison"]["same_combined_edge_count"],
        "same_diameter": p25["comparison"]["same_diameter"],
        "diameter": 8,
        "degree_histogram": {"8": 900},
        "combined_edge_count": 3600,
    },
    "working_position": [
        "The gap-1 orbit family, not a single labeled representative, is the current closure-bearing object.",
        "The Phase 15 preference for Orbit 2 remains meaningful as a pre-G60 local-balance result.",
        "The Phase 25 post-G60 global-distance result favors Orbit 1 under a different criterion.",
        "Because the selectors disagree, the project should not declare either orbit final.",
        "The next selector must combine local balance, closure, distance-shell behavior, and layer recoverability.",
    ],
    "safe_language": [
        "preference tension",
        "multi-invariant selector",
        "closure-bearing gap-1 family",
        "Orbit 2 local-balance preference",
        "Orbit 1 global-tightness preference",
    ],
    "avoid_language": [
        "Orbit 1 is the final law",
        "Orbit 2 is the final law",
        "Phase 25 overturns Phase 15",
        "Phase 15 proves Orbit 2 canonical",
        "closure alone selects the preferred orbit",
    ],
    "next_tests": [
        "Build a multi-invariant selector table for both gap-1 orbit representatives.",
        "Add all-root shell profile histograms, not only sampled roots.",
        "Audit layer recoverability: can G15 sectors, G60 copies, and G30 sheet residues be recovered after overlay?",
        "Compare automorphism or relabeling stability of the combined graphs.",
        "Export both combined candidates for renderer inspection.",
    ],
}

def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, data):
    lines = []
    lines.append("# " + data["name"])
    lines.append("")
    lines.append("Status: " + data["status"])
    lines.append("")
    lines.append("Warning: " + data["warning"])
    lines.append("")
    lines.append("## Pre-G60 selector")
    lines.append("")
    for k, v in data["pre_g60_selector"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Post-G60 selector")
    lines.append("")
    for k, v in data["post_g60_selector"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Common closure facts")
    lines.append("")
    for k, v in data["common_closure_facts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Working position")
    lines.append("")
    for item in data["working_position"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Safe language")
    lines.append("")
    for item in data["safe_language"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Avoid language")
    lines.append("")
    for item in data["avoid_language"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Next tests")
    lines.append("")
    for item in data["next_tests"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

write_json(OUT_JSON, obj)
write_md(OUT_MD, obj)
write_md(OUT_NOTE, obj)

print("wrote", OUT_JSON)
print("wrote", OUT_MD)
print("wrote", OUT_NOTE)
print("status=" + obj["status"])
print("pre_g60_preferred=" + str(phase15_preferred))
print("post_g60_tighter=" + str(post_g60_tighter))
print("orbit1_diameter8_vertices=" + str(orbit1_d8))
print("orbit2_diameter8_vertices=" + str(orbit2_d8))
print("next=phase27_multi_invariant_selector")
