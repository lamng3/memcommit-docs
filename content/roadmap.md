---
title: Roadmap
slug: roadmap
part: Project
order: 2
kicker: Project
description: What is built, and what comes next.
lede: Every feature in the plan is built and tested. Next are the gaps the benchmarks found.
---

## Built

The log-structured store, the declared structure, episodic sessions, derived notes with an index and agent tools, offline consolidation, the cache and its policies, compaction of memories and of the log, recall, the blackboard, audit, the server, a demo, and two benchmarks.

## Next

- **A model-backed extractor.** The built-in extractor finds about half the facts in the benchmark, and a perfect one reaches 1.000. A language model behind the `Extractor` signature is the largest open gain.
- **Deduplication across paths.** Near-duplicates are merged only within a directory.
- **Meaning, not words.** The lexical index cannot match a paraphrase that shares no words with the query. `VectorIndex` can; the benchmark does not yet test it.
- **Recorded conversations.** Both benchmarks are synthetic. The same harness should run on recorded conversations, with a model as reader.
- **A provider adapter** from `Knowledge.tools()` to a provider's tool format.

New work starts as an experiment: a recorded workload or a policy to compare, measured and written to `results/`.
