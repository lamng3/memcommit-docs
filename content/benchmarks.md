---
title: Benchmarks
slug: benchmarks
part: Reference
order: 3
kicker: Reference
description: What the two benchmarks measure and what they found.
lede: Both benchmarks are synthetic, so they show behaviour, not real-world accuracy. Both are deterministic and need no model.
---

## Does memory help?

`python examples/memory_benchmark.py` writes `results/memory/`. 20 users chat with an assistant over 8, 32, or 64 sessions each. Facts come up in passing, one is a request to remember, 40% of users move cities later, and the rest is chatter with distractors. Half the statements are in forms the built-in extractor is built for and half are paraphrases it cannot parse. Each user is then asked their current city, dog, drink, and locker code. A recency-aware reader answers from whatever each configuration retrieves: right if the latest-mentioned value the user ever gave is the current one. Means over 3 seeds.

| Configuration | 8 sessions | 32 sessions | 64 sessions | Context words at 64 |
|:--|:--:|:--:|:--:|--:|
| none | 0.000 | 0.000 | 0.000 | 0 |
| full history in context | 1.000 | 1.000 | 1.000 | 1,358 |
| episodic search only | 0.958 | 0.958 | 0.958 | 20 |
| notes from dreaming only | 0.492 | 0.512 | 0.487 | 15 |
| episodic + notes | 0.942 | 0.971 | 0.958 | 35 |
| notes from dreaming, oracle extractor | 1.000 | 1.000 | 1.000 | 12 |
| episodic + notes, oracle extractor | 1.000 | 1.000 | 1.000 | 33 |

What it shows:

- Search over the record reads about 20 words where the full history needs up to 1,358, and is right 96% of the time. Its misses are facts that changed.
- With a perfect extractor the notes are right every time from 12 words, because the later statement supersedes the old note. With the built-in rule extractor, which parses half the phrasings, they are right about half the time, and the two tiers together only match search alone. The extractor is the limit, not the pipeline.
- Saving by tool call alone catches only explicit requests, so it scores about 0.11 to 0.15.

:::warning
The paraphrases were written to share a stem with the questions, which favours lexical search, and the first version of this benchmark gave the extractor text written to match it and scored 1.000, which was circular. Both are stated in `results/memory/README.md`.
:::

## Which eviction policy?

`python examples/policy_benchmark.py` writes `results/policies/`. A synthetic agent-shaped workload (60 tasks writing 6 trace steps each, then 472 skewed reuses) is replayed through the real store under each policy, and the hit rate of working memory is measured at capacities 16, 32, and 64, with the cost in log records and replay time.

| Policy | Hit rate, cap 16 | cap 32 | cap 64 |
|:--|:--:|:--:|:--:|
| FIFO | 0.506 | 0.551 | 0.602 |
| LRU | 0.642 | 0.744 | 0.828 |
| LFU | 0.354 | 0.460 | 0.606 |
| Forgetting curve | 0.648 | 0.771 | 0.867 |
| ARC | 0.551 | 0.663 | 0.763 |
| Learned (online logistic) | 0.627 | 0.742 | 0.803 |

The forgetting curve does best under the cap and also writes the fewest log records, since every miss is a page-in and an eviction. LFU and 2Q do poorly because this workload reuses fresh trace steps often, and both evict memories used only once first. Which policy wins depends on the workload, which is why policies are pluggable and the benchmark can replay a recorded one (`AccessLog(record=True)`, then `bench.from_access_log`).
