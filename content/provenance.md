---
title: Provenance and invalidation
slug: provenance
part: Internals
order: 2
kicker: Internals
description: How derived_from drives invalidation, including reads that found nothing.
lede: Provenance is the lever the rest of MemCommit pulls. When a premise goes bad, everything built on it goes stale in one transaction.
---

## derived_from

`derived_from` holds memory ids and outside references (`doc:handbook@3`, `file:sha256...`). `invalidate(refs, reason)` marks stale every live memory reachable through the reference index, in one transaction. A client that versions something outside the store (a document, a knowledge base, a model) records the version as a reference, and invalidating the version invalidates what was built on it.

## Retraction

A commit that retracts a live memory marks stale everything built on it, directly or through a read whose result included it: work built on a premise that was withdrawn as wrong no longer holds. Memories written by the commit itself are left alone.

## Reads are provenance too

An answer derives from the memories it read, but it also depends on the ones it looked for and did not find. "No notes about this topic" is built on an empty read, and the first note must undo it. So a reference can name a read: `query_ref("note", topic="light")`. An agent derives from it next to the memories the read returned. When a commit brings a memory live, the store finds the reads that memory now belongs to and marks everything built on them stale, in the same transaction.

Only additions need this. A memory that drops out of a read was returned by it, so whatever used it already derives from it directly. Over-invalidation is cheap: work redone with the same result restores the same memory id.

## In sessions and notes

A reply records the memories it read in `derived_from`. A note records the session and turns it came from. A summary records the steps it folds. So retracting a spoofed session stales the notes learned from it and the replies that used those notes, with no extra code.

## Memories are values

A memory's id hashes its kind, key, body, source, scope, importance, and `derived_from`. A body cannot be changed without its id changing, so tampering shows up on load and in `verify`.
