from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "json"
OUT_MD = ROOT / "artifacts" / "md"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_MD.mkdir(parents=True, exist_ok=True)

phase14_path = OUT_JSON / "p900_phase14_orbit_family_comparison.json"
phase14 = json.loads(phase14_path.read_text(encoding="utf-8"))

profiles = phase14["profiles"]

scored = []

for name, profile in profiles.items():
    length_hist = profile["length_closure_histogram"]
    per_length_scores = {}

    total_local_balance_score = 0
    max_length_gap = 0
    perfectly_balanced_lengths = 0

    for length, counts in sorted(length_hist.items(), key=lambda item: int(item[0])):
        identity = counts.get("identity_closure", 0)
        half_turn = counts.get("half_turn_closure", 0)
        drift = counts.get("orientation_drift", 0)
        gap = abs(identity - half_turn)

        total_local_balance_score += gap
        max_length_gap = max(max_length_gap, gap)

        if gap == 0 and drift == 0:
            perfectly_balanced_lengths += 1

        per_length_scores[length] = {
            "identity_closure": identity,
            "half_turn_closure": half_turn,
            "orientation_drift": drift,
            "length_balance_gap": gap,
        }

    scored.append({
        "family": name,
        "half_turn_set": profile["half_turn_set"],
        "total_identity_closures": profile["identity_closure_count"],
        "total_half_turn_closures": profile["half_turn_closure_count"],
        "total_orientation_drift": profile["orientation_drift_count"],
        "total_balance_gap": profile["identity_half_turn_balance_gap"],
        "local_balance_score": total_local_balance_score,
        "max_length_gap": max_length_gap,
        "perfectly_balanced_length_count": perfectly_balanced_lengths,
        "per_length_scores": per_length_scores,
    })

ranked = sorted(
    scored,
    key=lambda row: (
        row["total_orientation_drift"],
        row["total_balance_gap"],
        row["local_balance_score"],
        row["max_length_gap"],
        -row["perfectly_balanced_length_count"],
        row["family"],
    )
)

winner = ranked[0]

summary = {
    "name": "P900 Phase 15 Local Balance Score",
    "status": "sandbox_audit",
    "warning": "This selects a preferred representative by local balance score only. It does not prove a final P900 law.",
    "source": "p900_phase14_orbit_family_comparison.json",
    "scoring_rule": "For each candidate family, sum abs(identity_closure - half_turn_closure) across each cycle length.",
    "ranking_rule": [
        "minimize orientation drift",
        "minimize total identity/half-turn balance gap",
        "minimize local balance score",
        "minimize max per-length gap",
        "maximize count of perfectly balanced lengths"
    ],
    "ranked_families": ranked,
    "preferred_by_local_balance": winner,
    "first_read": [
        "Both preferred orbit representatives remain tied at total balance gap 1 with zero drift.",
        "Phase 15 breaks the tie using local balance by cycle length.",
        "The lower local balance score is preferred as a representative for the next external-surface tests.",
        "This does not eliminate the other orbit family."
    ],
}

json_path = OUT_JSON / "p900_phase15_local_balance_score.json"
md_path = OUT_MD / "p900_phase15_local_balance_score.md"

json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

lines = []
lines.append("# P900 Phase 15 Local Balance Score")
lines.append("")
lines.append("Status: sandbox audit")
lines.append("")
lines.append("Warning: this selects a preferred representative by local balance score only. It does not prove a final P900 law.")
lines.append("")
lines.append("## Scoring rule")
lines.append("")
lines.append(summary["scoring_rule"])
lines.append("")
lines.append("## Ranking")
lines.append("")
for idx, row in enumerate(ranked, start=1):
    lines.append(f"### Rank {idx}: {row['family']}")
    lines.append("")
    lines.append(f"- half-turn set: {row['half_turn_set']}")
    lines.append(f"- total identity closures: {row['total_identity_closures']}")
    lines.append(f"- total half-turn closures: {row['total_half_turn_closures']}")
    lines.append(f"- total orientation drift: {row['total_orientation_drift']}")
    lines.append(f"- total balance gap: {row['total_balance_gap']}")
    lines.append(f"- local balance score: {row['local_balance_score']}")
    lines.append(f"- max length gap: {row['max_length_gap']}")
    lines.append(f"- perfectly balanced length count: {row['perfectly_balanced_length_count']}")
    lines.append(f"- per-length scores: {row['per_length_scores']}")
    lines.append("")
lines.append("## Preferred by local balance")
lines.append("")
lines.append(f"- family: {winner['family']}")
lines.append(f"- half-turn set: {winner['half_turn_set']}")
lines.append(f"- local balance score: {winner['local_balance_score']}")
lines.append("")
lines.append("## First read")
lines.append("")
for item in summary["first_read"]:
    lines.append(f"- {item}")
lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")

print("wrote", json_path)
print("wrote", md_path)
print("preferred_by_local_balance=" + winner["family"])
print("preferred_half_turn_set=" + str(winner["half_turn_set"]))
for row in ranked:
    print(
        row["family"] +
        " total_gap=" + str(row["total_balance_gap"]) +
        " local_balance_score=" + str(row["local_balance_score"]) +
        " max_length_gap=" + str(row["max_length_gap"]) +
        " balanced_lengths=" + str(row["perfectly_balanced_length_count"])
    )
