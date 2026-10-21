---
title: API at a glance
slug: api
part: Reference
order: 2
kicker: Reference
description: The main names MemCommit exports, by what they are for.
lede: Everything is imported from `memcommit`. The docstrings in each module are the full reference.
---

## Store

| Name | Purpose |
|:--|:--|
| `memcommit.open(path)` | A `MemoryStore` on a SQLite (`.db`) or JSON-lines (`.jsonl`) log. |
| `MemoryStore` | `transaction`, `put`, `find`, `latest`, `get`, `invalidate`, `rollback_to`, `as_of`, `history`, `move`, `refresh`, `save_snapshot`, `guard`, `subscribe`, `defer`. |
| `Memory`, `Record`, `Commit`, `State` | The values and the fold. |
| `query_ref(kind, key, scopes, **where)` | A reference to a read. |
| `Rejected` | Raised when a guard refuses a commit. |

## Structure

| Name | Purpose |
|:--|:--|
| `Schema`, `Kind` | Declare kinds; `attach`, `record`, `put`, `audit`, `describe`, `load`, `version`. |
| `check_body` | The JSON-schema subset validator. |

## Sessions, notes, dreaming

| Name | Purpose |
|:--|:--|
| `Session`, `Episodes` | Episodic memory. |
| `Knowledge` | Notes: `add`, `update`, `delete`, `read`, `ls`, `index`, `search`, `fetch`, `tools`, `call`, `take_reads`. |
| `Dreamer`, `Learning`, `Change`, `DreamReport`, `heuristic_extractor` | Offline consolidation. |
| `Trace`, `trace` | Runs as typed steps. |
| `Compactor`, `outline` | Traces into summaries. |

## Working memory and recall

| Name | Purpose |
|:--|:--|
| `TieredMemory`, `AccessLog`, `by_scope`, `by_trace` | The cache and its tiers. |
| `FIFO`, `LRU`, `LFU`, `TwoQueue`, `ARC`, `Forgetting`, `Scored`, `TTL`, `Learned` | Eviction policies. |
| `AccessCount`, `ImportanceAtLeast`, `KindIn`, `AnyOf`, `AllOf`, `Never` | Promotion policies. |
| `Recall`, `LexicalIndex`, `VectorIndex`, `AnnIndex`, `CacheSync` | Search. |

## Agents and defense

| Name | Purpose |
|:--|:--|
| `AgentSession`, `scope_guard` | An agent's view, and the write rule. |
| `Blackboard`, `Agent`, `Step` | Coordination. |
| `verify`, `lineage`, `blast_radius`, `quarantine`, `diff`, `provenance_guard`, `seal` | Audit. |

## Storage and processes

| Name | Purpose |
|:--|:--|
| `MemoryEngine`, `JsonlEngine`, `SqliteEngine`, `Engine`, `ENGINES` | Where the log lives. |
| `memcommit.storage` | `compact`, `ArchivedOlderThan`, `AutoSeal`, `check_seal`. |
| `memcommit.server` | `MemoryServer`, `RemoteStore`. |
| `AsyncMemoryStore` | Commits in a worker thread. |

## Measurement

| Name | Purpose |
|:--|:--|
| `memcommit.bench` | Replay writes and uses under any policy. |
| `memcommit.evaluation` | `make_workload`, `evaluate`, `table`: the memory benchmark. |
