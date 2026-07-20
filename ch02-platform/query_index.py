import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

endpoint = os.environ["SEARCH_ENDPOINT"]
credential = DefaultAzureCredential()
search_client = SearchClient(endpoint=endpoint, index_name="hello-index",
                             credential=credential)

# --- Full-text query ---
results = search_client.search(search_text="how do I avoid leaking secrets")
for r in results:
    print(f"{r['@search.score']:.2f}  {r['title']}")

# --- Filtered query, selecting fields ---
results = search_client.search(
    search_text="*",
    filter="category eq 'security'",
    select=["title", "category"],
)
for r in results:
    print(f"{r['title']}  [{r['category']}]")

# --- Facets ---
results = search_client.search(search_text="*", facets=["category"])
for value in results.get_facets()["category"]:
    print(f"{value['value']}: {value['count']}")
