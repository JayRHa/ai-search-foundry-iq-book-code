<!-- jr-brand:start -->
<div align="center">
  <a href="https://jannikreinhard.com/">
    <img src="https://raw.githubusercontent.com/JayRHa/.github/main/assets/readme/brand-header.png" alt="Jannik Reinhard — Driving AI with passion" width="100%">
  </a>
  <h1>Azure AI Search &amp; Foundry IQ · Book Code</h1>
  <p><strong>Runnable code for the book &#x27;Azure AI Search and Foundry IQ: Grounding Enterprise AI on Your Own Data&#x27; by Jannik Reinhard — organized by chapter, keyless.</strong></p>
  <p>
  <a href="https://jannikreinhard.com/"><img src="https://img.shields.io/badge/Website-146CDD?style=flat-square&amp;logo=wordpress&amp;logoColor=white" alt="Website"></a>
  <a href="https://github.com/JayRHa"><img src="https://img.shields.io/badge/GitHub-081427?style=flat-square&amp;logo=github&amp;logoColor=white" alt="GitHub"></a>
  <a href="https://www.linkedin.com/in/jannik-r/"><img src="https://img.shields.io/badge/LinkedIn-0795FF?style=flat-square&amp;logo=linkedin&amp;logoColor=white" alt="LinkedIn"></a>
  <a href="https://x.com/jannik_reinhard"><img src="https://img.shields.io/badge/X-081427?style=flat-square&amp;logo=x&amp;logoColor=white" alt="X"></a>
  <a href="https://www.youtube.com/@jannikreinhard"><img src="https://img.shields.io/badge/YouTube-146CDD?style=flat-square&amp;logo=youtube&amp;logoColor=white" alt="YouTube"></a>
  </p>
  <p><sub>Driving AI with passion · Microsoft Foundry · Intune · Azure</sub></p>
</div>
<!-- jr-brand:end -->

## About This Repository

Every code listing from the book **Azure AI Search and Foundry IQ** by
[Jannik Reinhard](https://jannikreinhard.com) — the REST calls, the Python, the
index / indexer / data source / skillset definitions, and the queries — as a file
you can run against your own service instead of retyping it from the page.

The repo is **organized by chapter**. Each folder matches a chapter of the book and
holds the listings from it, grouped by kind:

- **`.json`** — index, indexer, data source, skillset, and knowledge-base definitions.
- **`.http`** — REST calls in [VS Code REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) format (also easy to translate to `curl`).
- **`.py`** — the SDK examples (`azure-search-documents`, `azure-ai-projects`, `azure-ai-evaluation`, `openai`).
- **`.sh` / `.bicep`** — the Azure CLI and infrastructure snippets.

## Keyless from the first line

Nothing here uses an admin key or a query key. Every Python example authenticates
with **`DefaultAzureCredential`**, which resolves to your `az login` / VS Code
identity locally and to a managed identity in Azure — the same code in both places.
The REST samples use a **bearer token** you mint with
`az account get-access-token --scope https://search.azure.com/.default`.
Chapter 13 explains why disabling local (key) auth entirely is the right default and
how to grant the data-plane roles (`Search Index Data Reader` /
`Search Index Data Contributor`) that replace it.

There are **no secrets in this repository**. Every endpoint, resource id, and
deployment name is a placeholder — supply your own through environment variables.

## Start Here

```bash
git clone https://github.com/JayRHa/ai-search-foundry-iq-code
cd ai-search-foundry-iq-code

az login
python -m pip install -r requirements.txt

# Point at your own service (see the full list below)
export SEARCH_ENDPOINT="https://<your-service>.search.windows.net"

python ch02-platform/create_index.py
python ch02-platform/load_documents.py
python ch02-platform/query_index.py
```

## Environment variables

Copy `.env.example` and fill in your own values. The variables the code reads:

| Variable | Used for |
|---|---|
| `SEARCH_ENDPOINT` | Your search service, e.g. `https://<service>.search.windows.net` |
| `SEARCH_INDEX` | Target index name for push / query examples |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI / Foundry endpoint for embeddings and the LLM judge |
| `AZURE_OPENAI_JUDGE_DEPLOYMENT` | Strong model deployment used by the evaluators (Ch. 11) |
| `PROJECT_ENDPOINT` | Foundry project endpoint, `https://<res>.services.ai.azure.com/api/projects/<project>` |
| `SEARCH_CONNECTION_NAME` | Name of the Azure AI Search connection inside the Foundry project (Ch. 12) |
| `SEARCH_INDEX_NAME` | Index the grounded agent retrieves from (Ch. 12) |

The **embedding deployment name** (e.g. `text-embedding-3-large`) and the chat
deployment (e.g. `gpt-4.1-mini`) appear inline in the JSON/Python listings — change
them to match your own deployments. API versions are pinned inside each file to the
version verified while writing the book.

## Chapters

| | Chapter | What is in it |
|---|---|---|
| 2 | [Azure AI Search — The Platform](ch02-platform) | Create the service keyless, and a first end-to-end "hello index" |
| 4 | [Data Sources and Ingestion](ch04-data-sources) | Push model, blob data source, index, indexer, deletion detection |
| 5 | [Chunking and Integrated Vectorization](ch05-chunking) | Split skill, embedding skill, vectorizer, index projections |
| 6 | [Index Design](ch06-index-design) | Vector fields, HNSW, analyzers, scoring profiles, a worked schema |
| 7 | [Skillsets and Enrichment](ch07-skillsets) | Custom Web API skill, enrichment cache, an OCR → entities → embed skillset |
| 8 | [Full-Text, Vector, and Hybrid Search](ch08-queries) | BM25, Lucene syntax, vector, pre-filter, hybrid, citation shaping |
| 9 | [The Semantic Ranker](ch09-semantic-ranker) | Semantic configuration, captions and extractive answers |
| 10 | [Agentic Retrieval and Foundry IQ Knowledge Bases](ch10-agentic-retrieval) | Knowledge source, knowledge base, `retrieve`, attaching it to an agent |
| 11 | [Debugging and Evaluating Retrieval](ch11-debugging-eval) | Analyze Text, a labeled set, recall/MRR/nDCG, and Foundry RAG evaluators |
| 12 | [Grounding Foundry Agents](ch12-grounding-agents) | Ground an agent on an index and read the citations back |
| 13 | [Security](ch13-security) | Kill the keys, RBAC, managed identity, and permission trimming |
| 14 | [Performance, Scale, and Cost](ch14-performance-cost) | Scaling, vector compression, and a worked monthly cost model |

Chapters 1, 3, and 15 are conceptual and carry no standalone code listings.

## This area moves fast

Azure AI Search and Foundry IQ ship changes constantly — API versions, model names,
SKUs, quotas, and preview/GA status all drift. The book's content was verified against
Microsoft's public documentation in mid-2026. **This repository is where I keep the
code current** after printing, so if a listing here differs from the page, the repo is
the newer one. Always recheck current availability, limits, and prices before a
production decision.

## License

MIT — see [LICENSE](LICENSE). Provided as-is for educational use; test in a
non-production environment first.
