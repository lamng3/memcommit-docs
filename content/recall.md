---
title: Search and recall
slug: recall
part: Using MemCommit
order: 5
kicker: Using MemCommit
description: Find memories by relevance, recency, and importance.
lede: Recall keeps an index in step with the store, so a stale memory is never recalled, and scores hits by relevance, recency, and importance.
---

## Search

```python
from memcommit import Recall

recall = Recall(store, tiers=tiers)           # tiers is optional
hits = recall.search("speed of light", k=3, kinds=["fact"], scopes=["shared"], where={"unit": "km/s"})
for hit in hits:
    print(hit.memory.key, hit.score, hit.relevance, hit.recency, hit.importance)
```

The score is a weighted sum of relevance (from the index), recency (decay per log record since the memory last changed), and importance. Filters: `kinds`, `scopes`, `tiers` (short and long by default; `None` searches all, including the archive), and `where` (body fields). With `tiers` given to `Recall`, hits are touched, which is how recall feeds the replacement policies; pass `touch=False` to leave counts alone.

## Indexes

| Index | Needs | Notes |
|:--|:--|:--|
| `LexicalIndex` | nothing | BM25 over the memory's kind, key, and body text. Lowercase terms, a small stopword list dropped, a light stemmer so `live`, `lives`, and `lived` agree. |
| `VectorIndex(embed)` | an embedding function | Cosine similarity. `embed` maps a list of texts to a list of vectors. |
| `AnnIndex(embed, dimensions)` | an embedding function | Approximate cosine search by random-hyperplane LSH with multi-probe, for many vectors. |

Every index is a `Cache`: `CacheSync` admits memories as they go live and evicts them when they stop holding, so a stale or retracted memory is never recalled.

:::note
The lexical index matches words, not meaning. A paraphrase that shares no words with the query is not found; use `VectorIndex` for that. The benchmark in [Benchmarks](benchmarks.html) is built so its paraphrases share words with the questions, which favours lexical search.
:::

## Search across both tiers

`Knowledge.search(query, k, where)` searches notes (`derived`), what was said and done (`episodic`), or both (`all`), and returns plain dictionaries. See [Notes](notes.html).
