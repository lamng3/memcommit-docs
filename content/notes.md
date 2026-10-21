---
title: Notes
slug: notes
part: Using MemCommit
order: 3
kicker: Using MemCommit
description: Derived memory: notes at paths, an index to read first, and five tools a model can call.
lede: Notes are what was learned, short enough to read at the start of a session. Each records the episodes it came from.
---

## Write and read notes

```python
from memcommit import Knowledge

notes = Knowledge(store, "assistant")
notes.add("user/alice/city", "Alice lives in Lyon.", tags=["profile"], derived_from=[turn.id])
notes.update("user/alice/city", "Alice moved to Paris.")
notes.read("user/alice/city")          # the live note
notes.ls("user/alice")                 # live notes under a path
notes.delete("user/alice/pet", "it was wrong")
```

A path is a note's key. `add` raises if a live note is already there, and `update` raises if there is none.

## Updates supersede, deletes retract

The log is immutable, so an update writes a new version and marks the old one stale. By default everything derived from the old version goes stale with it, since it was built on something that changed; pass `cascade=False` for a typo fix. Writing the same text again changes nothing. `delete` retracts: the note was wrong, and what was built on it falls too.

## The index

```python
print(notes.index(max_chars=4000))
```

```text
# Memory index

4 notes. Use search_memory to find more, fetch_memory to read one.

## user/alice
- city: alice lives in Lyon. [profile]
- dog: alice's dog is Rex. [profile]
```

The index is generated on demand, by directory, with each note's title (or first line) and tags. It is sized to a budget: the most important and most recent notes are kept first, and the tail says how many were left out. Inject it at the start of a session.

## Search and fetch

```python
notes.search("where does alice live", k=5, where="derived")   # notes
notes.search("allergic chicken", where="episodic")            # what was said and done
notes.search("cat", where="all")                              # both, by score
notes.fetch("user/alice/city")                                # a note, in full
notes.fetch(session.id)                                       # a session id returns its transcript
```

`search` spans both tiers, so an agent can recover detail a note dropped. `fetch` takes a note path or any memory id.

## Tools for a model

`notes.tools()` returns five tool specs, each with a `name`, a `description`, and an `input_schema`: `add_memory`, `update_memory`, `delete_memory`, `search_memory`, and `fetch_memory`. `notes.call(name, arguments, session=session)` runs one and, with a session, records the call and its result in it. The shape is provider-neutral; an adapter maps it to a provider's format.

`notes.take_reads()` returns the ids read since the last call, to pass as `used` to `session.agent_says`.
