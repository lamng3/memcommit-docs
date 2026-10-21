---
title: Dreaming
slug: dreaming
part: Using MemCommit
order: 4
kicker: Using MemCommit
description: An offline pass that turns finished sessions into notes and keeps the notes tidy.
lede: An agent that saves notes by tool call only remembers what it thought to save. A dreaming pass finds what was implied, and maintains the store.
---

## Run a pass

```python
from memcommit import Dreamer

dreamer = Dreamer(store)                  # or Dreamer(store, extractor=my_model_extractor)
dreamer.run(dry_run=True).changes         # what it would do, without writing
report = dreamer.run()                    # do it
dreamer.undo(report)                      # take it back, if nobody else has written since
```

A pass reads the sessions that ended since the last pass, asks an extractor for the learnings in each, and writes them as notes derived from the session and the turns they came from. Then it maintains the store.

## What a pass does

| Step | Effect |
|:--|:--|
| Extract | Each learning becomes a note at its path, derived from the session and its source turns. |
| Conflicts | A learning whose path holds a different note replaces it. The old version goes stale, with what was built on it. The last statement in a session wins. |
| Duplicates | Live notes in the same directory with word overlap of at least 0.85 are merged: the most important is kept, the rest go to the archive. |
| Oversized | A note over `max_chars` (1200) is split at paragraph breaks into `-part-N` notes derived from it, and the original goes to the archive. |

## Extractors

An `Extractor` is a function from a `Session` to a list of `Learning(path, text, title, tags, importance, sources)`. The built-in `heuristic_extractor` needs no model. It finds statements the user made about where they live, "my X is Y", "I prefer Y", and "remember that Y", and it records a sequence of two or more tool calls that ended well as a playbook. The memory tools' own calls are not counted. A language model is a function with the same signature.

:::warning
The built-in extractor parses only the phrasings it has patterns for. On the synthetic benchmark it finds about half of the facts, and an oracle extractor finds all of them. See [Benchmarks](benchmarks.html). Pass a model-backed extractor for real use.
:::

## When to run

```python
dreamer.due(min_sessions=3)       # have enough sessions ended?
dreamer.attach(min_sessions=3)    # run a pass whenever enough sessions have ended
```

`memcommit dream memory.db` runs one from the command line, and `--dry-run` previews it.

## What a pass records

A pass writes a `dream` memory recording the log position it covered, derived from the sessions it read. The next pass starts from the highest position recorded, counting records of any status, so a pass whose source session was later retracted is not run again. `dreamer.watermark()` returns it.

## Repair and undo

Every edit is a transaction with provenance. Retract a bad session and the notes learned from it go stale. `undo(report)` rolls the log back to before the pass using compensating records, so history is kept, and refuses if any other agent has written since. An undone pass is not retried automatically.
