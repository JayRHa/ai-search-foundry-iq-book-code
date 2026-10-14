<!-- jr-brand:start -->
<p align="center">
  <a href="https://jannikreinhard.com/">
    <img src="https://raw.githubusercontent.com/JayRHa/.github/main/assets/readme/brand-header.png" alt="Jannik Reinhard — I help enterprises ship secure AI agents" width="100%">
  </a>
</p>
<p align="center">
  <a href="https://jannikreinhard.com/">Website</a> ·
  <a href="https://www.linkedin.com/in/jannik-r/">LinkedIn</a> ·
  <a href="https://x.com/jannik_reinhard">X</a> ·
  <a href="https://www.youtube.com/@jannikreinhard">YouTube</a>
</p>
<!-- jr-brand:end -->

# Chapter 10 — Agentic Retrieval and Foundry IQ Knowledge Bases

Foundry IQ's knowledge base plans a query, runs several searches in parallel over a
knowledge source (your existing index), reranks, and returns a merged, cited answer.

## Order to run the `.http` files

All calls need a bearer token scoped to the search service. Get one with
[`get_search_token.sh`](get_search_token.sh) and paste it where the files expect
`{{accessToken}}`.

1. [`create_knowledge_source.http`](create_knowledge_source.http) — a knowledge source over an existing search index.
2. [`create_knowledge_base.http`](create_knowledge_base.http) — the knowledge base that ties the source to a chat model and answer synthesis.
3. [`retrieve_answer_synthesis.http`](retrieve_answer_synthesis.http) — call `retrieve` with a conversation and get a synthesized, cited answer.
4. [`retrieve_intents.http`](retrieve_intents.http) — the lower-level `intents` shape when you want to drive the sub-queries yourself.
5. [`attach_kb_to_agent.py`](attach_kb_to_agent.py) — expose the knowledge base to a Foundry agent as an MCP tool.

## Reading the response

The `retrieve` call returns three things worth knowing. The **answer** comes back as
an assistant message whose text is a JSON array of cited references:

```json
"response": [
  {
    "role": "assistant",
    "content": [
      { "type": "text",
        "text": "[{\"ref_id\":\"0\",\"title\":\"Data Security Whitepaper\",\"content\":\"All customer data is encrypted at rest with AES-256 on every plan...\"}]" }
    ]
  }
]
```

The **activity** log shows the query plan — what it planned, every sub-search it ran,
and the tokens/latency each step cost. This is your bill and your debugging trace in
one place:

```json
"activity": [
  { "type": "modelQueryPlanning", "id": 0, "modelName": "gpt-4.1-mini",
    "inputTokens": 1876, "outputTokens": 94, "elapsedMs": 1902 },
  { "type": "searchIndex", "id": 1, "knowledgeSourceName": "kb-docs-ks",
    "count": 12, "elapsedMs": 210,
    "searchIndexArguments": { "search": "Business plan data encryption at rest" } },
  { "type": "searchIndex", "id": 2, "knowledgeSourceName": "kb-docs-ks",
    "count": 9, "elapsedMs": 198,
    "searchIndexArguments": { "search": "Enterprise plan encryption at rest comparison" } },
  { "type": "searchIndex", "id": 3, "knowledgeSourceName": "kb-docs-ks",
    "count": 7, "elapsedMs": 205,
    "searchIndexArguments": { "search": "customer-managed keys plan upgrade requirement" } },
  { "type": "modelAnswerSynthesis", "id": 4, "modelName": "gpt-4.1-mini",
    "inputTokens": 5310, "outputTokens": 288, "elapsedMs": 3401 }
]
```

A **references** array (omitted here) carries the full source chunks behind each
`ref_id` so you can render citations.

<!-- jr-brand-footer:start -->
---

[Articles and guides](https://jannikreinhard.com/) · [Repository index](https://github.com/JayRHa/.github/blob/main/REPOSITORIES.md)
<!-- jr-brand-footer:end -->
