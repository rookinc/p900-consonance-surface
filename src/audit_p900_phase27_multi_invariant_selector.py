from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

PHASE15 = ART_JSON / "p900_phase15_local_balance_score.json"
PHASE25 = ART_JSON / "p900_phase25_gap1_orbits_after_g60.json"
PHASE26 = ART_JSON / "p900_phase26_preference_tension_checkpoint.json"

OUT_JSON = ART_JSON / "p900_phase27_multi_invariant_selector.json"
OUT_MD = ART_MD / "p900_phase27_multi_invariant_selector.md"
OUT_NOTE = NOTES / "phase27_multi_invariant_selector.md"

p15 = json.loads(PHASE15.read_text(encoding="utf-8"))
p25 = json.loads(PHASE25.read_text(encoding="utf-8"))
p26 = json.loads(PHASE26.read_text(encoding="utf-8"))

phase15_rows = {}
for row in p15.get("ranking", []):
    name = row.get("family") or row.get("name")
    if name:
        phase15_rows[name] = row

# Fallback from the generated Phase 15 shape if no ranking key exists.
if not phase15_rows:
    pref = p15.get("preferred_by_local_balance")
    if isinstance(pref, dict):
        phase15_rows[pref["family"]] = pref

audits = {row["name"]: row for row in p25["candidate_audits"]}

candidate_names = [
    "gap1_orbit_1_representative",
    "gap1_orbit_2_representative",
]

# Phase 15 values from known artifact if ranking was not exposed in a simple shape.
phase15_fallback = {
    "gap1_orbit_1_representative": {
        "local_balance_score": 17,
        "max_length_gap": 8,
        "perfectly_balanced_length_count": 2,
        "total_balance_gap": 1,
    },
    "gap1_orbit_2_representative": {
        "local_balance_score": 13,
        "max_length_gap": 7,
        "perfectly_balanced_length_count": 3,
        "total_balance_gap": 1,
    },
}

def get_p15(name, key):
    row = phase15_rows.get(name) or phase15_fallback.get(name) or {}
    return row.get(key, phase15_fallback[name][key])

def get_hist_value(hist, key):
    return int(hist.get(str(key), hist.get(key, 0)))

selector_rows = []
for name in candidate_names:
    row25 = audits[name]
    ecc = row25["eccentricity_histogram"]

    local_balance_score = int(get_p15(name, "local_balance_score"))
    max_length_gap = int(get_p15(name, "max_length_gap"))
    balanced_lengths = int(get_p15(name, "perfectly_balanced_length_count"))
    total_balance_gap = int(get_p15(name, "total_balance_gap"))

    diameter8_vertices = get_hist_value(ecc, 8)
    eccentricity6_vertices = get_hist_value(ecc, 6)

    selector_rows.append({
        "name": name,
        "half_turn_set": row25["half_turn_set"],
        "identity_set": row25["identity_set"],
        "closes_after_g60": row25["connected"],
        "degree_histogram": row25["degree_histogram"],
        "combined_edge_count": row25["combined_edge_count"],
        "diameter": row25["diameter_if_connected"],
        "local_balance_score": local_balance_score,
        "max_length_gap": max_length_gap,
        "perfectly_balanced_length_count": balanced_lengths,
        "total_balance_gap": total_balance_gap,
        "eccentricity_histogram": row25["eccentricity_histogram"],
        "diameter8_vertices": diameter8_vertices,
        "eccentricity6_vertices": eccentricity6_vertices,
    })

def winner_min(key):
    best = min(r[key] for r in selector_rows)
    names = [r["name"] for r in selector_rows if r[key] == best]
    return {"criterion": key, "winning_value": best, "winners": names}

def winner_max(key):
    best = max(r[key] for r in selector_rows)
    names = [r["name"] for r in selector_rows if r[key] == best]
    return {"criterion": key, "winning_value": best, "winners": names}

criteria = [
    winner_min("local_balance_score"),
    winner_min("max_length_gap"),
    winner_max("perfectly_balanced_length_count"),
    winner_min("diameter8_vertices"),
    winner_max("eccentricity6_vertices"),
]

scorecard = {r["name"]: 0 for r in selector_rows}
for c in criteria:
    for name in c["winners"]:
        scorecard[name] += 1 / len(c["winners"])

if scorecard["gap1_orbit_1_representative"] > scorecard["gap1_orbit_2_representative"]:
    provisional_selector = "gap1_orbit_1_representative"
elif scorecard["gap1_orbit_2_representative"] > scorecard["gap1_orbit_1_representative"]:
    provisional_selector = "gap1_orbit_2_representative"
else:
    provisional_selector = "tie"

obj = {
    "phase": 27,
    "name": "P900 Phase 27 Multi-Invariant Selector",
    "status": "multi_invariant_selector_checkpoint",
    "warning": "This is a selector checkpoint, not a final P900 law or uniqueness proof.",
    "inputs": {
        "phase15": str(PHASE15),
        "phase25": str(PHASE25),
        "phase26": str(PHASE26),
    },
    "selector_rows": selector_rows,
    "criteria": criteria,
    "scorecard": scorecard,
    "provisional_selector": provisional_selector,
    "interpretation": [
        "Both gap-1 orbit representatives remain closure-bearing after internal G60 import.",
        "Orbit 2 remains favored by pre-G60 local cycle-balance measures.",
        "Orbit 1 is favored by post-G60 global tightness measures.",
        "The multi-invariant selector records this tension rather than erasing it.",
        "A final selector should wait for layer recoverability, all-root shells, and automorphism/relabeling tests.",
    ],
    "safe_language": [
        "multi-invariant selector checkpoint",
        "provisional selector",
        "closure-bearing candidates",
        "local-balance criterion",
        "global-tightness criterion",
    ],
    "avoid_language": [
        "final P900 law",
        "unique P900 graph",
        "canonical representative selected",
        "Orbit 1 defeats Orbit 2",
        "Orbit 2 defeats Orbit 1",
    ],
    "next_tests": [
        "Phase 28 all-root shell profile comparison.",
        "Phase 29 layer recoverability audit.",
        "Phase 30 combined graph export for Aletheos renderer.",
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
    lines.append("## Selector table")
    lines.append("")
    for row in data["selector_rows"]:
        lines.append("### " + row["name"])
        lines.append("")
        for key in [
            "half_turn_set",
            "identity_set",
            "closes_after_g60",
            "degree_histogram",
            "combined_edge_count",
            "diameter",
            "local_balance_score",
            "max_length_gap",
            "perfectly_balanced_length_count",
            "total_balance_gap",
            "eccentricity_histogram",
            "diameter8_vertices",
            "eccentricity6_vertices",
        ]:
            lines.append(f"- {key}: {row[key]}")
        lines.append("")
    lines.append("## Criteria winners")
    lines.append("")
    for c in data["criteria"]:
        lines.append(f"- {c['criterion']}: {c['winners']} at {c['winning_value']}")
    lines.append("")
    lines.append("## Scorecard")
    lines.append("")
    for k, v in data["scorecard"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Provisional selector")
    lines.append("")
    lines.append(str(data["provisional_selector"]))
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    for item in data["interpretation"]:
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
print("scorecard=" + str(scorecard))
print("provisional_selector=" + str(provisional_selector))
print("next=phase28_all_root_shell_profile_comparison")
