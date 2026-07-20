# push_documents.py — send documents straight to the index (push model).
# Keyless: DefaultAzureCredential resolves a managed identity in Azure,
# or your az login / VS Code identity locally. No admin key anywhere.
import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

endpoint = os.environ["SEARCH_ENDPOINT"]        # https://<service>.search.windows.net
index_name = os.environ["SEARCH_INDEX"]          # e.g. "product-manuals"

client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=DefaultAzureCredential(),
)

documents = [
    {
        "@search.action": "mergeOrUpload",   # upsert: insert or update by key
        "id": "manual-0007",
        "title": "Series 7 pump — maintenance guide",
        "content": "Depressurize the system before removing the housing...",
        "category": "maintenance",
        "lastUpdated": "2026-06-30T09:00:00Z",
    },
    {
        "@search.action": "delete",           # remove a document by its key
        "id": "manual-0003",
    },
]

result = client.upload_documents(documents=documents)
succeeded = sum(1 for r in result if r.succeeded)
print(f"{succeeded}/{len(result)} document actions succeeded")
