from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

# 1. Resolve the CURRENT user's group object IDs (from Microsoft Graph),
#    e.g. ["8f4a...", "b21c...", "all-employees-guid"].
user_group_ids = get_user_groups_from_graph(user_token)

# 2. Build an OData security filter: keep docs whose group_ids
#    intersect the user's groups. search.in() is the efficient way
#    to test membership against a collection field.
group_filter = " or ".join(
    f"group_ids/any(g: g eq '{gid}')" for gid in user_group_ids
)

client = SearchClient(
    endpoint="https://my-search-svc.search.windows.net",
    index_name="knowledge",
    credential=DefaultAzureCredential(),
)

results = client.search(
    search_text="parental leave policy",
    filter=group_filter,          # <-- the trimming happens here
    top=5,
)
