# Chapter 11 — Search Explorer, Debugging, and Evaluating Retrieval

## Debugging

- [`search_explorer_query.json`](search_explorer_query.json) — a hybrid + semantic query body to paste into Search Explorer for a ten-second sanity check.
- [`analyze_text.http`](analyze_text.http) — the Analyze Text API: see exactly what an analyzer does to a query string before it hits the index.

## Evaluating retrieval

- [`labels.jsonl`](labels.jsonl) — a tiny labeled set (query → graded relevant docs). This is the foundation everything else stands on.
- [`eval_retrieval.py`](eval_retrieval.py) — measure recall@k, precision@k, MRR, and nDCG against a live index.
- [`eval_generation.py`](eval_generation.py) — score groundedness, relevance, and retrieval with the Foundry `azure-ai-evaluation` evaluators (LLM-as-judge).
- [`document_retrieval_evaluator.py`](document_retrieval_evaluator.py) — the `DocumentRetrievalEvaluator` for graded, score-aware retrieval metrics.

`eval_retrieval.py` prints something like:

```text
  queries      : 87
  recall@5     : 0.812
  precision@5  : 0.298
  MRR          : 0.734
  nDCG@5       : 0.681
```

Low precision@k is expected here — with only a handful of graded-relevant docs per
query, most of the top-k slots can't be "relevant" even for a perfect ranker. Watch
recall@k, MRR, and nDCG@k over time instead, and always compare against the *same*
labeled set.
