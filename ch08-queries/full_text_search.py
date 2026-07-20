from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

credential = DefaultAzureCredential()
client = SearchClient(
    endpoint="https://<service>.search.windows.net",
    index_name="kb-index",
    credential=credential,
)

results = client.search(
    search_text="reset my password",
    search_fields=["title", "chunk"],
    select=["chunk_id", "parent_id", "title", "chunk"],
    top=5,
    include_total_count=True,
)

print(f"total matches: {results.get_count()}")
for r in results:
    print(round(r["@search.score"], 3), r["title"])
