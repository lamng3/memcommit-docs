---
title: Concepts
slug: concepts
part: Getting started
order: 3
kicker: Getting started
description: Memories, the log, status, tiers, and provenance.
lede: A memory is an immutable value. Everything that changes about it is a record in a log, and state is what replaying the log gives.
---

## Memories

A `Memory` is a JSON value with a `kind` (what sort of thing it is), a `key` (what it is about), a `body`, a `source` (the agent that wrote it), a `scope` (who may read it), an `importance`, and `derived_from` (what it was built on). Its id is a hash of all of that, so writing the same memory twice names the same memory, and work redone with the same result restores what was there.

## The log

Every change is a record: `put`, `restore`, `stale`, `retract`, or `move`. Records are numbered (LSN) and grouped into transactions, which are all or nothing. The store's state is a fold over the log, so `as_of(lsn)` rebuilds any past state, and rollback writes compensating records instead of erasing anything.

## Status

Status says whether a memory holds.

| Status | Meaning |
|:--|:--|
| `live` | It holds. |
| `stale` | Something it was built on no longer holds. Redone work may bring it back. |
| `retracted` | It was wrong. |

## Tier

Tier says where a memory sits, which is what retrieval and policies act on.

| Tier | Holds |
|:--|:--|
| `short` | Working memory, bounded: new memories, an agent's context. A cache. |
| `mid` | Optional: evicted memories grouped into segments (by trace). |
| `long` | Consolidated memories and summaries. |
| `archive` | Everything evicted or compacted. Searched on request; paged back in on use. |

Status and tier are independent: a stale long-term memory is still long-term.

## Provenance

`derived_from` names the memories (and outside references like `doc:handbook@3`) a memory was built on. When one of them goes stale or is retracted, everything built on it goes stale, transitively, in one transaction. A memory can also derive from a read (`query_ref`), so work that saw "nothing known" is redone when something becomes known. See [Provenance](provenance.html).

## Two kinds of memory

Episodic memory is the record: sessions, turns, and tool calls, as they happened. Derived memory is what was learned: notes at paths. A note names the episodes it came from, so the detail is one `fetch` away, and a bad episode takes its notes with it.
