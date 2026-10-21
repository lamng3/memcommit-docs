---
title: Audit and defense
slug: audit
part: Using MemCommit
order: 8
kicker: Using MemCommit
description: Verify the log, trace what a memory was built on, and repair damage exactly.
lede: Shared memory is an attack surface. MemCommit does not decide what is malicious, but it makes a defender's work exact.
---

## Tools

| Tool | What it does |
|:--|:--|
| `verify(store)` | Replays the log and returns problems: altered bodies, records out of order, provenance to memories that did not exist, writes into another agent's scope. An empty list is ok. |
| `lineage(store, id)` | Everything a memory was built on. |
| `blast_radius(store, refs)` | Everything built on a reference, in any status. |
| `quarantine(store, ids, reason)` | Retracts suspects and marks what was built on them stale, in one transaction. |
| `diff(store, a, b)` | Memories whose status or tier changed between two LSNs. |
| `provenance_guard()` | Rejects at write time a memory built on a memory that is missing or no longer holds. |
| `seal(store)` | Writes a hash chain over the log; `verify` rechecks it, so a deleted or reordered record is caught. |
| `scope_guard` | An agent writes only to `shared` or its own scopes. |

## A typical repair

```python
from memcommit import blast_radius, quarantine, verify

affected = blast_radius(store, [bad_observation.id])    # what the bad observation reached
quarantine(store, [bad_observation.id], "tool was compromised")
assert verify(store) == []
```

The agents on a blackboard then redo only the work that went stale. Because notes and replies record what they were derived from, the same repair reaches [notes](notes.html) learned from a spoofed session.

## Why it works

Memories are content-addressed, so an altered body no longer hashes to its id. The log is append-only, so `verify` can replay it for what a well-behaved store could not have written. Provenance is a graph, so the reach of a bad memory is a query. See [Provenance](provenance.html).
