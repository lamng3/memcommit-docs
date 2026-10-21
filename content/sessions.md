---
title: Sessions
slug: sessions
part: Using MemCommit
order: 2
kicker: Using MemCommit
description: Episodic memory: record conversations and tool calls as they happen.
lede: A session is a trace with conversational helpers. Every turn, tool call, and result is its own memory, committed as it happens.
---

## Record a session

```python
from memcommit import Session

with Session.start(store, "assistant", user="alice") as session:
    session.user_says("I live in Lyon.")
    lookup = session.wrap(search_web, "search_web")      # calls recorded with their results
    lookup(query="weather in Lyon")
    session.agent_says("Noted.")
```

Leaving the block ends the session `ok`, or `error` if it raised. Each step commits on its own, so a crash keeps what was said. `Session.open(store, root_id)` reads one back, `session.transcript()` lists its turns, calls, and results in order, and `session.text()` renders them as text.

## Tool calls

`session.call(tool, arguments, run)` runs `run(**arguments)`, recording an `action` before and an `observation` after, or an `error` if it raised (and re-raising). `session.wrap(function, name)` returns the function with every call recorded, as a plugin would.

## Replies derive from what they read

```python
session.agent_says("Alice lives in Lyon.", used=notes.take_reads())
```

`used` are the memories the reply was built on. If one is later retracted, the reply goes stale.

## Find sessions

```python
from memcommit import Episodes

episodes = Episodes(store)
episodes.sessions(user="alice", ended=True)   # oldest first
episodes.new_since(lsn)                        # sessions that ended after a point in the log
```

`new_since` is what an offline pass reads. See [Dreaming](dreaming.html).

## What is stored

A session is a `trace` root with the task `session` and the user in its inputs. User and agent turns are `message` steps with a `role`; calls are `action` steps; results are `observation` steps. Nothing is distilled away, so detail a summary dropped can still be fetched.
