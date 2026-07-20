from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

# No key anywhere. The credential resolves to your dev login locally,
# or the app's managed identity in Azure — same code, both places.
credential = DefaultAzureCredential()
client = SearchClient(
    endpoint="https://my-search-svc.search.windows.net",
    index_name="knowledge",
    credential=credential,
)

results = client.search(search_text="onboarding checklist", top=5)
