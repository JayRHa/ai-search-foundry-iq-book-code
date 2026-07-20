from azure.search.documents.models import VectorizableTextQuery

query = "reset my password"

vq = VectorizableTextQuery(
    text=query, k_nearest_neighbors=50, fields="text_vector",
)

results = client.search(
    search_text=query,              # BM25 half
    search_fields=["title", "chunk"],
    vector_queries=[vq],            # vector half
    select=["chunk_id", "parent_id", "title", "chunk"],
    top=10,
)
for r in results:
    print(round(r["@search.score"], 4), r["title"])
