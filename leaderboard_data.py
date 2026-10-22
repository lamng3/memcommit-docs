#!/usr/bin/env python3
"""Export the memory benchmark for the manual's arena page.

    python3 leaderboard_data.py [../memcommit/results/memory/2026-10-21.json]

One board per number of sessions per user. Each configuration is ranked by how many of the questions it answers
correctly; the page shows what it had to read to do so. Nothing is recomputed here beyond picking fields.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT.parent / "memcommit/results/memory/2026-10-21.json")
REFERENCE = {"none", "full context"}


def main():
    data = json.loads(SOURCE.read_text())
    boards = []
    for sessions, rows in sorted(data["sessions"].items(), key=lambda kv: int(kv[0])):
        boards.append(
            {
                "id": f"s{sessions}",
                "name": f"{sessions} sessions",
                "sub": f"{data['users']} users, {sessions} sessions each, seeds {data['seeds']}. Each user states facts that change, then is asked about them.",
                "metric": "accuracy", "metricLabel": "Accuracy", "fmt": "f3",
                "columns": [
                    {"key": "words", "label": "Words read", "fmt": "f1"},
                    {"key": "records", "label": "Log records", "fmt": "int"},
                    *({"key": a, "label": a.capitalize(), "fmt": "f2"} for a in ("city", "dog", "drink", "locker")),
                ],
                "rows": [
                    {
                        "name": r["name"],
                        "group": "reference" if r["name"] in REFERENCE else "memcommit",
                        "tag": "oracle extractor: an upper bound" if "oracle" in r["name"] else "",
                        "score": r["accuracy"],
                        "values": {"words": r["context_words"], "records": r["log_records"], **r["by_attribute"]},
                    }
                    for r in rows
                ],
            }
        )
    out = {
        "note": f"Synthetic workload, deterministic, no model. Words read is the context a question needed. Oracle rows use an extractor that sees the truth, so they bound what the pipeline could do; the rule-based extractor is the limit today. From {SOURCE.name}.",
        "groups": {"memcommit": {"label": "MemCommit", "ours": True}, "reference": {"label": "Reference"}},
        "boards": boards,
    }
    (ROOT / "leaderboard-data.json").write_text(json.dumps(out))
    print(f"{len(boards)} boards")


if __name__ == "__main__":
    main()
