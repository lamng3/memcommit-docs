---
title: Agents and scopes
slug: agents
part: Using MemCommit
order: 7
kicker: Using MemCommit
description: Share one memory between agents: scopes, sessions, and the blackboard.
lede: Several agents can read each other's memories as premises. Scopes decide who may read and write, and a blackboard coordinates the work.
---

## Scopes

A memory's scope says who may read it. `shared` is for every agent; a scope named after an agent (`planner`) or under it (`planner/drafts`) is that agent's own. An `AgentSession` reads `shared` plus the agent's own scopes and stamps every write with the agent's name.

```python
from memcommit import AgentSession, scope_guard

store.guard(scope_guard)                       # an agent may put only into shared or its own scopes
planner = AgentSession(store, "planner", reads=["research"])
planner.put("plan", "trip", {"steps": ["book"]}, scope="planner/drafts")
planner.find(kind="plan")
```

`scope_guard` is enforced at commit for every agent. The system agent may write anywhere.

## The blackboard

```python
from memcommit import Blackboard

class Writer:
    name = "writer"
    consumes = frozenset({"finding"})

    def handle(self, finding, tx, session):
        tx.put("brief", finding.key, {"text": "..."}, derived_from=[finding.id])

board = Blackboard(store, [Researcher(), Writer()])
board.run()
```

Agents consume kinds of memory and write results. An agent's results and a receipt commit together, so work is done exactly once, survives a restart, and is redone when its inputs go stale. An agent that names what it `produces` runs upstream of its consumers. A failing agent writes nothing but an `error` memory in its own scope.

## Traces and handoffs

`memcommit.trace(store, agent, task)` records a run as a root and a tree of typed steps (`thought`, `action`, `observation`, `message`, `result`, `error`). `t.handoff(agent, task)` starts another agent's sub-trace derived from a message step. See [Sessions](sessions.html) for the conversational form.
