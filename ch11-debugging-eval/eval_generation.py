# eval_generation.py — score groundedness, relevance, and retrieval with Foundry evaluators.
# pip install azure-ai-evaluation
import os
from azure.ai.evaluation import (
    evaluate, GroundednessEvaluator, RelevanceEvaluator, RetrievalEvaluator,
)

# The LLM-judge model. Use a strong model here — the judge's quality caps yours.
model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "azure_deployment": os.environ["AZURE_OPENAI_JUDGE_DEPLOYMENT"],
    "api_version": "2025-01-01-preview",
}

groundedness = GroundednessEvaluator(model_config)
relevance = RelevanceEvaluator(model_config)
retrieval = RetrievalEvaluator(model_config)

result = evaluate(
    data="rag_runs.jsonl",   # rows of {query, context, response}
    evaluators={
        "groundedness": groundedness,
        "relevance": relevance,
        "retrieval": retrieval,
    },
    evaluator_config={
        "groundedness": {"column_mapping": {
            "query": "${data.query}",
            "context": "${data.context}",
            "response": "${data.response}"}},
        "relevance": {"column_mapping": {
            "query": "${data.query}",
            "response": "${data.response}"}},
        "retrieval": {"column_mapping": {
            "query": "${data.query}",
            "context": "${data.context}"}},
    },
    output_path="./gen_eval_results.json",
)

print(result["metrics"])   # aggregate scores across the dataset
