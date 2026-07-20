from azure.ai.evaluation import DocumentRetrievalEvaluator

doc_retrieval = DocumentRetrievalEvaluator(
    ground_truth_label_min=0, ground_truth_label_max=3,
)

result = doc_retrieval(
    retrieval_ground_truth=[
        {"document_id": "sso-guide-07", "query_relevance_label": 3},
        {"document_id": "sso-guide-08", "query_relevance_label": 2},
    ],
    retrieved_documents=[
        {"document_id": "sso-guide-08", "relevance_score": 45.1},
        {"document_id": "faq-11",       "relevance_score": 35.8},
        {"document_id": "sso-guide-07", "relevance_score": 28.4},
    ],
)
print(result)   # -> ndcg@3, xdcg@3, fidelity, top1_relevance, holes, holes_ratio, ...
