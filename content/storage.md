---
title: The database underneath
slug: storage
part: Internals
order: 3
kicker: Internals
description: Log compaction, retention, snapshots, seals, and the server.
lede: MemCommit is a log-structured store, and it borrows a database's answers to a database's problems.
---

## Two levels of compaction

Memory compaction decides what agents see: finished traces fold into summaries, cold mid-term segments consolidate, summaries of the same task merge. It never deletes; it moves memories to the archive.

Log compaction decides what the disk holds. A memory's history can be long (put, stale, restore, stale, move), but replaying its state needs three records: the put, the last status change, and the last move. `storage.compact` keeps exactly those, as the original records, up to a horizon, and keeps every record after the horizon verbatim, so the folded log replays to the same state. That is the LSM move: rewrite the sorted history into something smaller that answers the same reads. The price is history inside the horizon.

```python
from memcommit.storage import ArchivedOlderThan, compact

report = compact(store, retention=ArchivedOlderThan(seconds=30 * 86400))
print(report.before, "->", report.after, "records; purged", len(report.purged))
```

## Retention

Purging is the one place a memory leaves the log. It happens only during log compaction, only for memories a retention policy names (`ArchivedOlderThan`, `KindsAfter`, or any `RetentionPolicy`), and only for memories with no record after the horizon. A `compaction` manifest lists them, so a later reference to a purged memory is known to be deliberate, not forged.

## Snapshots

```python
store.save_snapshot("state.json")
store = memcommit.open("memory.db", snapshot="state.json")   # replays only the records after it
```

A snapshot is the state as JSON. Opening from one reads only the records after it.

## Seals

`seal(store)` writes a hash chain over the log up to an LSN; `AutoSeal(store, every=1000)` seals every N records; `check_seal` rechecks the newest and `verify` rechecks all of them after the last compaction. Compaction invalidates every earlier seal by design, so the manifest stores the old log's chain and a new seal covers the new log.

## One writer, many readers

LSNs must come from one place. `python -m memcommit serve memory.db` runs a `MemoryServer` that owns the log and runs every commit, so guards hold across processes. `RemoteStore(url)` is a `MemoryStore` on it, and `store.refresh()` pulls commits other processes made. A refused commit raises `Rejected` in the client. `AsyncMemoryStore` commits in a worker thread, one at a time, for an event loop.
