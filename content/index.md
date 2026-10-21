---
title: Introduction
slug: index
part: Getting started
order: 1
kicker: MemCommit Manual
description: The MemCommit manual. MemCommit is a transactional memory layer for agents.
lede: MemCommit keeps what agents did and learned as memories in one append-only log, with provenance, tiers, a declared structure, and an offline pass that turns finished sessions into notes.
---

An agent that remembers needs two things. It needs the full record of what happened, so detail is never lost. It also needs short notes of what matters, so it can read what it knows in a few lines. MemCommit keeps both, in one log, and records where every note came from.

This manual describes how to install MemCommit, declare the structure of your memory, record sessions, keep and search notes, consolidate them offline, bound working memory, audit it, and run it from the command line. The last parts describe how it works inside and how the project is developed.

## What MemCommit does today

- Stores memories as immutable, content-addressed JSON values in an append-only log. Status (`live`, `stale`, `retracted`) and tier (`short`, `mid`, `long`, `archive`) come from replaying the log. See [Concepts](concepts.html).
- Checks every write against a memory structure you declare. See [Declare a memory structure](structure.html).
- Records sessions as they happen: each turn, tool call, and result. See [Sessions](sessions.html).
- Keeps notes at paths, with a generated index and five tools a model can call. See [Notes](notes.html).
- Consolidates sessions into notes offline, supersedes conflicting notes, merges duplicates, splits oversized ones, and can undo a pass. See [Dreaming](dreaming.html).
- Marks stale everything built on a premise that stops holding, in one transaction. See [Provenance](provenance.html).
- Bounds working memory with a cache and replacement policies, and compacts both memories and the log. See [Working memory](tiers.html) and [The database underneath](storage.html).

:::note
MemCommit is research software. Results so far are on synthetic workloads; see [Benchmarks](benchmarks.html).
:::

## Quick start

```text
git clone https://github.com/lamng3/memcommit.git
cd memcommit
pip install -e ".[dev]"
memcommit demo
```

The demo runs a scripted assistant, with no model and no network, through every part of the loop. See [Install and run the demo](install.html).
