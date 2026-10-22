---
title: Leaderboard
slug: leaderboard
part: Reference
order: 4
kicker: Reference
description: Memory configurations ranked by how many questions they answer correctly, and what they had to read to do it.
lede: The memory benchmark as a leaderboard: each configuration ranked by accuracy, with the words it read and the log it kept.
---

The board is honest about where the library stands. Reading the whole history answers everything but costs the most words. Searching the episodic record answers about 96% of questions from about 20 words. The notes a rule-based extractor writes reach about 49%, and the oracle rows show the same pipeline reaching 100% when the extractor is perfect, so extraction quality is the limit, not the pipeline.

<div data-arena data-src="leaderboard-data.json"></div>
<script src="arena.js"></script>

## How to read it

- **Accuracy** is the share of questions answered correctly, over the users and seeds shown.
- **Reference** rows are the two ends: no memory at all, and the full history in context.
- **Oracle** rows run an extractor that sees the truth. They are upper bounds for the notes pipeline, not results.
- Click a column to sort. Ranks stay with accuracy, so a sort does not change who is first.

See [Benchmarks](benchmarks.html) for the protocol and its caveats, including that the paraphrases favour lexical search.
