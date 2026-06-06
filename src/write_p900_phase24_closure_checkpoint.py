from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

PHASE23 = ART_JSON / "p900_phase23_combined_g60_external_graph.json"

OUT_JSON = ART_JSON / "p900_phase24_closure_checkpoint.json"
OUT_MD = ART_MD / "p900_phase24_closure_checkpoint.md"
OUT_NOTE = NOTES / "phase24_closure_checkpoint.md"

phase23 = json.loads(PHASE23.read_text(encoding="utf-8"))

counts = phase23["counts"]
checks = phase23["checks"]

checkpoint_ok = (
    checks.get("p900_vertex_count_is_900") is True
    and checks.get("g60_source_import_ok") is True
    and checks.get("external_edge_count_is_1800") is True
    and checks.get("internal_edge_count_is_1800") is True
    and checks.get("duplicate_edge_count_is_0") is True
    and checks.get("combined_edge_count_is_3600") is True
    and checks.get("degree_regular_8") is True
    and checks.get("connected") is True
)

obj = {
    "phase": 24,
    "name": "P900 Phase 24 Closure Checkpoint",
    "status": "closure_style_checkpoint_ok" if checkpoint_ok else "closure_checkpoint_needs_review",
    "warning": "This records a closure-style graph checkpoint, not a final P900 theorem or uniqueness proof.",
    "source_phase": str(PHASE23),
    "closure_style_claim": (
        "The preferred external P900 layer, when combined with 15 internal canonical G60 copies, "
        "forms a single connected 900-state graph."
    ),
    "numeric_checkpoint": {
        "vertex_count": counts["vertex_count"],
        "internal_edge_count": counts["internal_edge_count"],
        "external_edge_count": counts["external_edge_count"],
        "duplicate_edge_count": counts["duplicate_edge_count"],
        "combined_edge_count": counts["combined_edge_count"],
        "degree_histogram": counts["degree_histogram"],
        "component_count": counts["component_count"],
        "component_size_histogram": counts["component_size_histogram"],
        "connected": counts["connected"],
        "diameter_if_connected": counts["diameter_if_connected"],
    },
    "interpretation": [
        "At Phase 20, the external-only P900 scaffold decomposed into 30 doubled-G15 sheets.",
        "Phase 22 imported canonical G60 as a verified 60-vertex, 120-edge, 4-regular connected local body.",
        "Phase 23 overlaid 15 internal G60 copies with the preferred external P900 surface law.",
        "The resulting graph is connected, 8-regular, and has 3600 edges.",
        "Therefore 900 is now more than a visual exposure checkpoint: it is a connected body-plus-surface checkpoint for this construction.",
    ],
    "safe_language": [
        "closure-style checkpoint",
        "connected combined P900 candidate",
        "body-plus-surface graph",
        "external P900 scaffold plus internal G60 copies",
        "first positive closure audit",
    ],
    "avoid_language_until_further_tests": [
        "final P900 theorem",
        "unique P900 graph",
        "canonical P900 law",
        "proof that the preferred orbit is final",
        "proof that 900 is metaphysical closure",
    ],
    "next_tests": [
        "Compare against the second gap-1 orbit after G60 import.",
        "Audit shortest-path shell profiles from multiple roots in the combined graph.",
        "Check automorphism or relabeling stability of the combined construction.",
        "Test whether G15/G30/G60 layers remain recoverable after overlay.",
        "Export combined edge list for the Aletheos renderer.",
    ],
    "checkpoint_ok": checkpoint_ok,
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
    lines.append("## Closure-style claim")
    lines.append("")
    lines.append(data["closure_style_claim"])
    lines.append("")
    lines.append("## Numeric checkpoint")
    lines.append("")
    for k, v in data["numeric_checkpoint"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("checkpoint_ok: " + str(data["checkpoint_ok"]))
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
    lines.append("## Avoid language until further tests")
    lines.append("")
    for item in data["avoid_language_until_further_tests"]:
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
print("checkpoint_ok=" + str(checkpoint_ok))
print("connected=" + str(counts["connected"]))
print("degree_histogram=" + str(counts["degree_histogram"]))
print("diameter_if_connected=" + str(counts["diameter_if_connected"]))
