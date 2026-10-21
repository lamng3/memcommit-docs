---
title: Declare a memory structure
slug: structure
part: Using MemCommit
order: 1
kicker: Using MemCommit
description: Name the kinds of memory your project writes, and have every write checked against them.
lede: MemCommit's core knows no domain. A project declares its own kinds once, as a schema, and a commit guard enforces it for every writer.
---

## A schema of kinds

```python
from memcommit import Kind, Schema

schema = Schema(
    Kind("question", body={"type": "object", "required": ["text"]}),
    Kind(
        "answer",
        description="what an agent concluded",
        body={
            "type": "object",
            "required": ["text", "confidence"],
            "properties": {"confidence": {"type": "number", "minimum": 0, "maximum": 1}},
        },
        requires=("question",),
        scopes=("shared", "agent"),
        tier="long",
        importance=0.5,
    ),
    strict=True,
    name="support",
)
schema.attach(store)
```

`attach` adds the guard and records the schema in the log. From then on a commit that puts a memory out of line with its kind is rejected before it is written, with every problem named.

## What a kind says

| Field | Meaning |
|:--|:--|
| `body` | A JSON schema for the body. |
| `scopes` | Where it may be written: `shared`, `agent` (the writer's own scope or one under it), or any scope name. `None` allows any. |
| `requires` | Kinds it must be derived from. A memory of this kind must list at least one memory of each in `derived_from`. A premise written in the same commit counts. |
| `tier`, `importance` | Defaults that `schema.put(store, agent, kind, key, body)` fills in. |

`strict=True` rejects kinds the schema does not declare. The kinds MemCommit writes itself (traces and their steps, summaries, receipts, seals, the compaction manifest, notes, dream records, the schema) are always allowed.

## The body schema

A small JSON-schema subset, with no dependency: `type` (`object`, `array`, `string`, `number`, `integer`, `boolean`, `null`, or a list), `properties`, `required`, `additionalProperties` (`false` to forbid extras), `items`, `enum`, `minimum`, `maximum`, `minLength`, `maxLength`, `minItems`, `maxItems`. A schema written in it is also valid JSON Schema.

## Provenance is declared with structure

`requires` is how a structure also says what a memory must be built on. An `answer` that names no `question` is rejected, so a memory cannot be written with its lineage missing, and invalidating a question reaches its answers.

## Evolving a schema

The schema is itself a memory. Recording a changed schema writes a new `schema` memory and marks the previous one stale, so `as_of(lsn)` shows which structure held when. `Schema.load(store, name)` reads the live one back, and `schema.version` is a short hash of its content.

Old data is not revalidated when the schema changes. `schema.audit(store)` returns the live memories that no longer conform, by id.

## Showing the structure

`schema.describe()` returns the structure as Markdown, one section per kind, which is what an agent can read to know what it may write.

:::note
Kinds other systems write to the same store are not checked unless `strict` is on. The Agentic Ontologist's `STRUCTURE` is declared this way: it checks `question`, `answer`, and agent-run steps, and leaves KROMA's and Aegis's kinds alone.
:::
