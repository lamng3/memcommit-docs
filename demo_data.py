#!/usr/bin/env python3
"""Run a small scenario on the real memcommit library and export its log for the manual's live demo.

The page replays the log in the browser. The one thing it cannot recompute is which
memories the library marks stale when one is retracted, so that is asked of the
library here, for every memory, and exported beside the log.
"""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "memcommit" / "src"))

import memcommit  # noqa: E402


def scenario(store):
    """(label, memory) in the order written. Each label is one line of the story."""
    story = []

    def put(label, kind, key, body, **kw):
        memory = store.put("assistant", kind, key, body, **kw)
        story.append(label)
        return memory

    s1 = put("Alice opens a session", "episode", "alice/1", {"text": "I live in Lyon and my dog is Rex."})
    city = put("Dreaming turns it into a note", "knowledge", "user/alice/city", {"text": "Alice lives in Lyon."}, derived_from=[s1.id])
    dog = put("...and another", "knowledge", "user/alice/dog", {"text": "Alice's dog is named Rex."}, derived_from=[s1.id])
    plan = put("The agent plans a trip from the city note", "plan", "alice/trip", {"text": "Book a train from Lyon."}, derived_from=[city.id])
    put("It drafts a message from the plan", "answer", "alice/msg", {"text": "Your train from Lyon is booked."}, derived_from=[plan.id])
    put("Mallory opens a session", "episode", "mallory/1", {"text": "I live in Atlantis."})
    return story


def main():
    with tempfile.TemporaryDirectory() as scratch:
        scratch = Path(scratch)
        store = memcommit.open(scratch / "demo.db")
        story = scenario(store)
        records = store.history()
        memories = {}
        for r in records:
            m = r.memory
            memories[m.id] = {"id": m.id, "kind": m.kind, "key": m.key, "text": m.body.get("text", ""), "from": list(m.derived_from)}
        log = [{"lsn": r.lsn, "txn": r.txn, "op": r.op, "id": r.memory.id, "note": story[i] if i < len(story) else ""} for i, r in enumerate(records)]

        cascades = {}
        for memory_id in memories:
            hit = [memory_id] + [m for m in store.state.dependents([memory_id]) if m != memory_id]
            cascades[memory_id] = hit
        out = {"memories": list(memories.values()), "log": log, "cascade": cascades, "verify": memcommit.audit.verify(store)}
    (ROOT / "site").mkdir(exist_ok=True)
    (ROOT / "demo-data.json").write_text(json.dumps(out, indent=1))
    print(f"{len(log)} records, {len(memories)} memories, verify={out['verify'] or 'ok'}")


if __name__ == "__main__":
    main()
