from azure.search.documents import SearchClient

search_client = SearchClient(endpoint=endpoint,
                             index_name="hello-index",
                             credential=credential)

documents = [
    {"id": "1", "title": "Retrieval beats fine-tuning",
     "content": "For most enterprise problems, grounding a model on your own "
                "data with retrieval is cheaper and fresher than fine-tuning.",
     "category": "concepts"},
    {"id": "2", "title": "What a search index is",
     "content": "An index is the searchable container your queries run against, "
                "defined by fields with attributes that control their behavior.",
     "category": "platform"},
    {"id": "3", "title": "Keyless by default",
     "content": "Use Entra ID roles and managed identities instead of admin keys "
                "so there is no shared secret to leak.",
     "category": "security"},
]

result = search_client.upload_documents(documents=documents)
print(f"Uploaded {len([r for r in result if r.succeeded])} documents")
