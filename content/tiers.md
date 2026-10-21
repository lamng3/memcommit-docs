---
title: Working memory
slug: tiers
part: Using MemCommit
order: 6
kicker: Using MemCommit
description: Bound short-term memory with a cache, replacement policies, promotion, and compaction.
lede: The store holds every memory; short-term memory holds the few an agent works with now. It is a cache, and its policies are pluggable.
---

## Configure the tiers

```python
from memcommit import (
    AccessCount, AnyOf, Compactor, ImportanceAtLeast, KeepFailed, KindIn, Scored, TieredMemory,
)

tiers = TieredMemory(
    store,
    capacity=64,                                   # per partition; a partition is a scope by default
    eviction=Scored(recency=1.0, importance=1.0, frequency=0.5),
    promotion=AnyOf(AccessCount(3), ImportanceAtLeast(0.8), KindIn(["decision"])),
    compactor=Compactor(store, policy=KeepFailed(records=5000), summarizer=my_summary),
    mid_capacity=256, heat_threshold=10.0,          # a mid-term tier of segments
    long_capacity=10_000,
)
tiers.touch([m.id for m in context])               # count a use; archived memories are paged back in
tiers.working(scopes=["shared", "planner"])        # what is in working memory
tiers.maintain()                                   # runs on its own when a partition goes over capacity
```

## What maintenance does

When a commit leaves a partition over capacity, `maintain()` runs after the commit, through `store.defer`:

1. Compact finished traces into long-term summaries.
2. Promote what the promotion policy selects to long-term.
3. Evict from each short-term partition over capacity, memories that no longer hold first, then the eviction policy's victims, to the archive (or to mid-term).
4. Trim long-term to its capacity, if it has one.

## Hits and misses

`touch` is a cache access: a hit when the memory is in short-term memory, a warm hit when it is in mid- or long-term, and a miss when it is archived or no longer holds. A missed live memory is paged back in, and eviction makes room. `tiers.stats` counts them.

## Policies

| Eviction | Idea |
|:--|:--|
| `FIFO`, `LRU`, `LFU` | The classics. |
| `TwoQueue`, `ARC` | Scan-resistant and adaptive (ghost lists). |
| `Forgetting` | An Ebbinghaus curve: what is used often or marked important fades slowest. |
| `Scored` | A weighted recency, importance, and frequency score. |
| `TTL` | A time to live by kind. |
| `Learned` | An online logistic model. |

Promotion policies are `AccessCount`, `ImportanceAtLeast`, `KindIn`, `AnyOf`, `AllOf`, and `Never`. A policy is any object with `victims(candidates, n, now)` or `select(candidates, now)`; a candidate carries the memory, its tier and status, and its use counts on a logical clock. Stateful policies are told about each use, eviction, and page-in.

## Mid-term segments

With `mid_capacity`, evicted memories wait in the `mid` tier grouped into segments (by trace). A segment past `heat_threshold` is promoted whole; while mid-term is over capacity, the coldest segment is consolidated into one summary and archived.

## Compaction of memories

`Compactor` turns a finished trace into a long-term `summary` derived from the root and every step, and moves the steps to the archive, in one transaction. Policies choose which traces: `FinishedTraces`, `OlderThan`, `KeepFailed`, `UnderPressure`. `Compactor.merge` folds summaries of the same task into one. A summarizer is any function from a `Trace` to JSON; `outline` needs no model.
