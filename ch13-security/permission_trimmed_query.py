import requests
from azure.identity import DefaultAzureCredential

# App identity — authorizes the CALL to the index (Search Index Data Reader).
app_token = DefaultAzureCredential().get_token(
    "https://search.azure.com/.default"
).token

# End-user token — the identity the results are TRIMMED to. In a web app this
# is the token you already hold for the signed-in user (on-behalf-of flow).
end_user_token = get_signed_in_user_token()

resp = requests.post(
    "https://my-search-svc.search.windows.net/indexes/knowledge/docs/search"
    "?api-version=2026-05-01-preview",
    headers={
        "Authorization": f"Bearer {app_token}",
        "x-ms-query-source-authorization": f"Bearer {end_user_token}",
        "Content-Type": "application/json",
    },
    json={"search": "parental leave policy", "select": "id,content", "top": 5},
)

# Every document in resp.json()["value"] is one THIS user is allowed to read.
for doc in resp.json()["value"]:
    print(doc["id"])
