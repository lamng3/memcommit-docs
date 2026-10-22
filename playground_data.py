#!/usr/bin/env python3
"""Export scenarios for the MemCommit playground's tests, from the real library.

    cd ../memcommit && uv run python ../memcommit-docs/playground_data.py

Each scenario is a seeded random sequence of puts, retractions, invalidations, and rollbacks run on a real memcommit store.
It is saved with the ids and log records the library produced, so the page's JavaScript port of the log (content-addressed
ids, restore-on-rewrite, cascading invalidation, compensating rollback) can be checked record by record.
"""

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "memcommit" / "src"))

import memcommit  # noqa: E402

KINDS = ["fact", "note", "plan", "answer"]
KEYS = ["a", "b", "c", "d", "e", "f"]
TEXTS = ["Lyon", "Paris", "Rex", "plum42", "a train", "naïve café", "x y"]
AGENTS = ["assistant", "researcher"]


def scenario(seed, steps=40):
    rng = random.Random(seed)
    store = memcommit.MemoryStore()
    ops, ids = [], []
    for _ in range(steps):
        roll = rng.random()
        live = [m for m in ids if store.status(m) == "live"]
        if roll < 0.55 or not ids:
            agent, kind, key, text = rng.choice(AGENTS), rng.choice(KINDS), rng.choice(KEYS), rng.choice(TEXTS)
            derived = sorted(rng.sample(ids, min(len(ids), rng.randint(0, 2)))) if ids else []
            memory = store.put(agent, kind, key, {"text": text}, derived_from=derived)
            if memory.id not in ids:
                ids.append(memory.id)
            ops.append({"op": "put", "agent": agent, "kind": kind, "key": key, "text": text, "derived": derived, "id": memory.id})
        elif roll < 0.70:
            target = rng.choice(ids)
            with store.transaction("assistant") as tx:
                tx.retract(target, "wrong")
            ops.append({"op": "retract", "agent": "assistant", "id": target, "reason": "wrong"})
        elif roll < 0.88 and live:
            refs = [rng.choice(live)]
            store.invalidate(refs, "premise changed")
            ops.append({"op": "invalidate", "refs": refs, "reason": "premise changed"})
        elif store.lsn > 2:
            lsn = rng.randint(1, store.lsn - 1)
            store.rollback_to(lsn, f"back to {lsn}")
            ops.append({"op": "rollback", "lsn": lsn, "reason": f"back to {lsn}"})
    records = [[r.lsn, r.txn, r.op, r.memory.id, r.agent, r.reason, r.tier] for r in store.history()]
    return {"seed": seed, "ops": ops, "records": records, "status": {m: store.status(m) for m in ids}, "tier": {m: store.tier(m) for m in ids}}


def main():
    out = {"scenarios": [scenario(seed) for seed in range(12)]}
    (ROOT / "playground-data.json").write_text(json.dumps(out, ensure_ascii=False))
    total = sum(len(s["records"]) for s in out["scenarios"])
    print(f"{len(out['scenarios'])} scenarios, {total} records")


if __name__ == "__main__":
    main()
