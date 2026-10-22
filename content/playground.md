---
title: Playground
slug: playground
part: Getting started
order: 3
kicker: Try it
description: Write memories into an append-only log in the browser, retract a premise, and watch what was built on it go stale.
lede: Write memories into an append-only log, say what each was derived from, retract a premise, and watch what was built on it go stale. Drag the log back in time, or roll it back.
---

:::warning
This playground runs a **JavaScript port of MemCommit's core**, not the library. MemCommit is Python. The port covers content-addressed memories, restore on rewrite, retraction and invalidation with their cascades, rollback by compensating records, and `as_of`, and its tests replay scenarios recorded from the Python library and compare every id and log record. It does not port query references, guards, tiers beyond the first, or sessions, notes, and dreaming. For those, run `memcommit demo` ([Install](install.html)).
:::

<div id="mplay" aria-label="Memory log playground">Loading the playground…</div>
<script src="pg.js"></script>
<script src="playground.js"></script>

## Things to try

1. **Load the demo** and retract the first episode (it was wrong). It is withdrawn as a premise, and everything live built on it goes stale in the same transaction; the unrelated episode stays live. **Mark stale** is the softer version for something that is merely outdated. That is [provenance](provenance.html).
2. **Write the same memory twice.** A live memory with identical content is not written again. Write one that was retracted and it is restored: the id is a hash of the content, so redoing work that comes out the same names the same memory.
3. **Drag the slider back** to see the state at an earlier log position, then press **Roll back**. The log is not rewritten: compensating records are appended, as in ARIES.
4. **Export the log** to read it as JSON.

## What it keeps

The operations you perform are saved in this browser (localStorage) and replayed when the page loads, so the log is the same after a reload. Clear the log to start again. Nothing is sent anywhere.
