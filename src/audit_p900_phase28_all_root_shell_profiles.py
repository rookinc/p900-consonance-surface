from pathlib import Path
from collections import Counter, deque
import json

ROOT = Path(__file__).resolve().parents[1]
ART_JSON = ROOT / "artifacts" / "json"
ART_MD = ROOT / "artifacts" / "md"
NOTES = ROOT / "notes"

PHASE25 = ART_JSON / "p900_phase25_gap1_orbits_after_g60.json"

OUT_JSON = ART_JSON / "p900_phase28_all_root_shell_profiles.json"
OUT_MD = ART_MD / "p900_phase28_all_root_shell_profiles.md"
OUT_NOTE = NOTES / "phase28_all_root_shell_profiles.md"

PETERSEN_EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
]

CANDIDATES = [
    {
        "name": "gap1_orbit_1_representative",
        "half_turn_set": [0, 1, 2, 3, 5],
    },
    {
        "name": "gap1_orbit_2_representative",
        "half_turn_set": [0, 1, 2, 3, 9],
    },
]

G60_PATH = ART_JSON / "p900_phase22_canonical_g60_import.json"

def vid(sector, local):
    return sector * 60 + local

def pair(a, b):
    return tuple(sorted((a, b)))

def shared_vertex(e1, e2):
    s = set(e1) & set(e2)
    if len(s) != 1:
        raise ValueError("bad Petersen line graph edge")
    return next(iter(s))

def line_graph_edges():
    rows = []
    for i, e1 in enumerate(PETERSEN_EDGES):
        for j in range(i + 1, len(PETERSEN_EDGES)):
            e2 = PETERSEN_EDGES[j]
            if set(e1) & set(e2):
                rows.append((i, j, shared_vertex(e1, e2)))
    return rows

def build_internal_edges(g60_edges):
    edges = set()
    for sector in range(15):
        for a, b in g60_edges:
            edges.add(pair(vid(sector, a), vid(sector, b)))
    return edges

def build_external_edges(half_turn_set):
    half = set(half_turn_set)
    edges = set()
    for i, j, sv in line_graph_edges():
        shift = 30 if sv in half else 0
        for x in range(60):
            edges.add(pair(vid(i, x), vid(j, (x + shift) % 60)))
    return edges

def adjacency(vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj

def shell_profile(root, adj):
    dist = {root: 0}
    q = deque([root])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)

    if len(dist) != len(adj):
        return None

    m = max(dist.values())
    hist = Counter(dist.values())
    return tuple(hist[i] for i in range(m + 1))

def audit_candidate(candidate, internal_edges):
    vertices = list(range(900))
    external_edges = build_external_edges(candidate["half_turn_set"])
    combined_edges = internal_edges | external_edges
    adj = adjacency(vertices, combined_edges)

    profile_counter = Counter()
    ecc_counter = Counter()
    sector_profile_counter = {}
    examples = {}

    for root in vertices:
        prof = shell_profile(root, adj)
        if prof is None:
            raise SystemExit("graph is not connected for " + candidate["name"])

        profile_counter[prof] += 1
        ecc_counter[len(prof) - 1] += 1

        sector = root // 60
        sector_profile_counter.setdefault(sector, Counter())
        sector_profile_counter[sector][prof] += 1

        examples.setdefault(prof, root)

    profiles = []
    for prof, count in profile_counter.most_common():
        profiles.append({
            "profile": list(prof),
            "count": count,
            "example_root": examples[prof],
        })

    sector_summary = {}
    for sector, counter in sorted(sector_profile_counter.items()):
        sector_summary[str(sector)] = {
            "distinct_profile_count": len(counter),
            "profile_counts": [
                {"profile": list(p), "count": c}
                for p, c in counter.most_common()
            ],
        }

    return {
        "name": candidate["name"],
        "half_turn_set": candidate["half_turn_set"],
        "identity_set": [x for x in range(10) if x not in set(candidate["half_turn_set"])],
        "vertex_count": 900,
        "combined_edge_count": len(combined_edges),
        "distinct_shell_profile_count": len(profile_counter),
        "eccentricity_histogram": dict(sorted(ecc_counter.items())),
        "shell_profile_histogram": profiles,
        "sector_summary": sector_summary,
    }

def compact_profiles(profiles, max_items=12):
    return profiles[:max_items]

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path, obj):
    lines = []
    lines.append("# P900 Phase 28 All-Root Shell Profile Comparison")
    lines.append("")
    lines.append("Status: " + obj["status"])
    lines.append("")
    lines.append("Warning: " + obj["warning"])
    lines.append("")
    lines.append("## Comparison")
    lines.append("")
    for k, v in obj["comparison"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Candidate summaries")
    lines.append("")
    for row in obj["candidate_summaries"]:
        lines.append("### " + row["name"])
        lines.append("")
        lines.append(f"- half_turn_set: {row['half_turn_set']}")
        lines.append(f"- identity_set: {row['identity_set']}")
        lines.append(f"- vertex_count: {row['vertex_count']}")
        lines.append(f"- combined_edge_count: {row['combined_edge_count']}")
        lines.append(f"- distinct_shell_profile_count: {row['distinct_shell_profile_count']}")
        lines.append(f"- eccentricity_histogram: {row['eccentricity_histogram']}")
        lines.append("")
        lines.append("Top shell profiles:")
        lines.append("")
        for p in compact_profiles(row["shell_profile_histogram"]):
            lines.append(f"- count {p['count']}, example root {p['example_root']}: {p['profile']}")
        lines.append("")
    lines.append("## First read")
    lines.append("")
    for item in obj["first_read"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

g60 = json.loads(G60_PATH.read_text(encoding="utf-8"))
internal_edges = build_internal_edges([tuple(e) for e in g60["g60_edges"]])

summaries = [audit_candidate(c, internal_edges) for c in CANDIDATES]

by_name = {s["name"]: s for s in summaries}
o1 = by_name["gap1_orbit_1_representative"]
o2 = by_name["gap1_orbit_2_representative"]

comparison = {
    "same_distinct_shell_profile_count": o1["distinct_shell_profile_count"] == o2["distinct_shell_profile_count"],
    "same_eccentricity_histogram": o1["eccentricity_histogram"] == o2["eccentricity_histogram"],
    "orbit1_distinct_shell_profile_count": o1["distinct_shell_profile_count"],
    "orbit2_distinct_shell_profile_count": o2["distinct_shell_profile_count"],
    "orbit1_eccentricity_histogram": o1["eccentricity_histogram"],
    "orbit2_eccentricity_histogram": o2["eccentricity_histogram"],
}

if comparison["same_distinct_shell_profile_count"] and comparison["same_eccentricity_histogram"]:
    status = "all_root_profiles_tied_basic"
else:
    status = "all_root_profiles_distinguish_gap1_orbits"

first_read = [
    "Phase 28 computes shell profiles from all 900 roots for both gap-1 orbit representatives.",
    "This strengthens Phase 25 by replacing sampled-root profiles with complete all-root shell data.",
]

if status == "all_root_profiles_distinguish_gap1_orbits":
    first_read.append("The all-root profile data distinguishes the two closure-bearing candidates.")
else:
    first_read.append("The all-root profile data does not distinguish the two candidates at this summary level.")

obj = {
    "phase": 28,
    "name": "P900 Phase 28 All-Root Shell Profile Comparison",
    "status": status,
    "warning": "This compares all-root shell profiles for two closure-bearing candidates. It is not a final selector.",
    "candidate_summaries": summaries,
    "comparison": comparison,
    "first_read": first_read,
}

write_json(OUT_JSON, obj)
write_md(OUT_MD, obj)
write_md(OUT_NOTE, obj)

print("wrote", OUT_JSON)
print("wrote", OUT_MD)
print("wrote", OUT_NOTE)
print("status=" + status)
for row in summaries:
    print(row["name"])
    print("  distinct_shell_profile_count=" + str(row["distinct_shell_profile_count"]))
    print("  eccentricity_histogram=" + str(row["eccentricity_histogram"]))
    print("  top_profile=" + str(row["shell_profile_histogram"][0]))
