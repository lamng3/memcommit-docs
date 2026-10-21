---
title: The log and the state
slug: log
part: Internals
order: 1
kicker: Internals
description: Records, transactions, guards, observers, and rollback.
lede: Status and tier are not stored on a memory. They are a fold over an append-only log, and every other feature is built on that.
---

## Records and state

A `Record` puts, restores, retracts, or marks stale one memory, or moves it between tiers, inside a transaction, by an agent, at a time. `State` applies records in LSN order and keeps three indexes: by (kind, key), from each reference to the memories derived from it, and from each kind to the reads over it. Replaying the log rebuilds exactly the state that wrote it, and `as_of(lsn)` is a replay that stops early.

## Transactions

All writes go through `store.transaction(agent)`. A transaction that raises writes nothing. Rewriting a live memory is a no-op, and a put of a known memory is a restore. On commit the store numbers the records, asks every guard, appends them to the engine in one call, applies them to the state, and then tells every observer.

## Guards before, observers after

Guards reject a commit before it happens: scopes, provenance, a declared schema, a defender's checks. Observers react after it: caches, tier policies, schedulers. Neither may commit during a commit. An observer that wants to write calls `store.defer(work)`, and the store runs the work once the commit is done, in order.

## Rollback is compensation

`rollback_to(lsn)` computes the state at that LSN and writes the records that move every memory back to its status and tier there, as ARIES does. Nothing is erased, so the log still shows what happened and what undid it.

## Engines

| Engine | Where the log lives |
|:--|:--|
| `MemoryEngine` | A list, for tests. |
| `JsonlEngine` | One fsynced JSON line per transaction; a torn final line is dropped. |
| `SqliteEngine` | One SQLite transaction per commit, WAL journaling. |

Another backend subclasses `Engine` (two methods: `append` and `records`; `records_after` and `rewrite` have defaults it may speed up) and registers in `ENGINES`. An engine can keep the log in an RDF store, so provenance questions become SPARQL: `SELECT ?m WHERE { ?m <urn:memcommit:derivedFrom> <urn:memcommit:m:4e33527c048490ae> . }`.
