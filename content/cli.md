---
title: Command line
slug: cli
part: Reference
order: 1
kicker: Reference
description: The memcommit command: run the demo, inspect and consolidate a store, serve it, verify and compact it.
lede: Every command takes a store path; the suffix picks the engine (.db for SQLite, .jsonl for JSON lines).
---

## Commands

| Command | What it does |
|:--|:--|
| `memcommit demo [--path demo.db]` | Run the end-to-end sample agent. With `--path`, keep its store. |
| `memcommit index memory.db [--agent assistant] [--max-chars 4000]` | Print the catalog of notes. |
| `memcommit search memory.db "query" [--where W] [-k 5] [--agent assistant]` | Search notes, episodes, or both; prints JSON. `W` is `derived` (default), `episodic`, or `all`. |
| `memcommit dream memory.db [--dry-run]` | Run an offline consolidation pass; lists each change. |
| `memcommit verify memory.db` | Replay the log and report problems. Prints `ok`; exits 1 on problems. |
| `memcommit stats memory.db` | Counts by status, tier, and kind. |
| `memcommit compact memory.db [--retain-archive-seconds N]` | Fold the log, purging old archived memories if asked. |
| `memcommit serve memory.db [--host 127.0.0.1] [--port 7340] [--snapshot state.json]` | Serve a store to agents in other processes. |

`python -m memcommit` is the same command.

## Example

```text
memcommit demo --path demo.db
memcommit stats demo.db
memcommit index demo.db
memcommit search demo.db "dog" --where all
memcommit dream demo.db --dry-run
memcommit verify demo.db
```
