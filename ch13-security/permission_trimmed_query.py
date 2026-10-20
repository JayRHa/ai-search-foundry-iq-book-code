"""Query an ACL-enabled index with separate application and user identities.

Set SEARCH_ENDPOINT, SEARCH_INDEX_NAME, and SEARCH_USER_ACCESS_TOKEN.
Supply the user token through secure runtime configuration. In a web app,
obtain it from the validated authentication flow. Never print or commit tokens.
"""
import os
import requests
from azure.identity import DefaultAzureCredential

def main():
    endpoint = os.environ["SEARCH_ENDPOINT"].rstrip("/")
    index = os.environ["SEARCH_INDEX_NAME"]
    user_token = os.environ["SEARCH_USER_ACCESS_TOKEN"]
    if not user_token.strip():
        raise ValueError("SEARCH_USER_ACCESS_TOKEN must contain an end-user access token")
    with DefaultAzureCredential() as credential:
        app_token = credential.get_token("https://search.azure.com/.default").token
        response = requests.post(
            f"{endpoint}/indexes/{index}/docs/search",
            params={"api-version": "2026-05-01-preview"},
            headers={
                "Authorization": f"Bearer {app_token}",
                "x-ms-query-source-authorization": user_token,
                "Content-Type": "application/json",
            },
            json={"search": "parental leave policy", "select": "id,content", "top": 5},
            timeout=30,
        )
        response.raise_for_status()
        for document in response.json()["value"]:
            print(document["id"])

if __name__ == "__main__":
    main()
