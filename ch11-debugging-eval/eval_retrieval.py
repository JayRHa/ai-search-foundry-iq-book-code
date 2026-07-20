# eval_retrieval.py — measure recall@k, precision@k, MRR, nDCG against a live index.
# pip install azure-search-documents azure-identity
import json
import math
from statistics import mean
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery

SERVICE = "https://<your-service>.search.windows.net"
INDEX = "kb-index"
K = 5                       # top-k you actually feed the model
KEY_FIELD = "doc_id"        # the field that matches doc_id in your labels

client = SearchClient(SERVICE, INDEX, credential=DefaultAzureCredential())


def search_ids(query: str, k: int) -> list[str]:
    """Run the same hybrid + semantic query your app uses; return ranked doc ids."""
    results = client.search(
        search_text=query,
        vector_queries=[VectorizableTextQuery(
            text=query, k_nearest_neighbors=50, fields="contentVector")],
        query_type="semantic",
        semantic_configuration_name="default",
        select=[KEY_FIELD],
        top=k,
    )
    return [doc[KEY_FIELD] for doc in results]


def dcg(grades: list[int]) -> float:
    return sum(g / math.log2(i + 2) for i, g in enumerate(grades))


def evaluate(labels_path: str, k: int = K) -> None:
    recalls, precisions, rrs, ndcgs = [], [], [], []
    with open(labels_path, encoding="utf-8") as fh:
        for line in fh:
            case = json.loads(line)
            gold = {r["doc_id"]: r.get("grade", 1) for r in case["relevant"]}
            ranked = search_ids(case["query"], k)

            hits = [d for d in ranked if d in gold]
            # recall@k and precision@k (binary relevance)
            recalls.append(len(hits) / len(gold) if gold else 0.0)
            precisions.append(len(hits) / k)
            # reciprocal rank of the first relevant hit
            rr = next((1 / (i + 1) for i, d in enumerate(ranked) if d in gold), 0.0)
            rrs.append(rr)
            # nDCG@k with graded labels
            gains = [gold.get(d, 0) for d in ranked]
            ideal = sorted(gold.values(), reverse=True)[:k]
            idcg = dcg(ideal)
            ndcgs.append(dcg(gains) / idcg if idcg else 0.0)

    print(f"  queries      : {len(recalls)}")
    print(f"  recall@{k}     : {mean(recalls):.3f}")
    print(f"  precision@{k}  : {mean(precisions):.3f}")
    print(f"  MRR          : {mean(rrs):.3f}")
    print(f"  nDCG@{k}       : {mean(ndcgs):.3f}")


if __name__ == "__main__":
    evaluate("labels.jsonl")
