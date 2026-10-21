---
title: Install and run the demo
slug: install
part: Getting started
order: 2
kicker: Getting started
description: Install MemCommit and run the end-to-end demo.
lede: Python 3.11 or newer, no runtime dependencies. The demo shows the whole loop in a few seconds.
---

## Install

```text
git clone https://github.com/lamng3/memcommit.git
cd memcommit
pip install -e ".[dev]"
```

`[dev]` adds pytest and ruff. The library itself has no dependencies.

## Run the demo

```text
memcommit demo
```

A scripted assistant talks to users over several sessions. The demo walks through eight steps:

1. The structure is declared once, and every write is checked against it.
2. Two users talk to the assistant; it keeps the full record of each session.
3. Dreaming: an offline pass extracts what was implied, with provenance back to the turns.
4. The next session starts with the index, then answers from notes.
5. A fact changes; the pass supersedes the note, and what was built on the old one goes stale.
6. An episode turns out to be spoofed; the notes learned from it go stale.
7. A synthetic benchmark answers whether memory helps.
8. The record verifies.

`memcommit demo --path demo.db` keeps the store, so you can inspect it afterwards with [the command line](cli.html).

## Use it from Python

```python
import memcommit
from memcommit import Dreamer, Knowledge, Session

store = memcommit.open("memory.db")               # SQLite; .jsonl works too; MemoryStore() is in memory

with Session.start(store, "assistant", user="alice") as session:
    session.user_says("I live in Lyon, and my dog is named Rex.")
    session.agent_says("Noted.")

Dreamer(store).run()                              # turns the session into notes
notes = Knowledge(store, "assistant")
print(notes.index())                              # the catalog of what the assistant knows
print(notes.search("where does alice live"))
```

## Tests

```text
pytest
ruff check . && ruff format --check .
python examples/memory_benchmark.py              # writes results/memory/
python examples/policy_benchmark.py              # writes results/policies/
```
