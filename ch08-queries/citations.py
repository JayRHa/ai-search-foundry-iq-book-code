results = client.search(
    search_text=query,
    vector_queries=[vq],
    select=["chunk_id", "parent_id", "title", "chunk"],  # never text_vector
    top=8,
)

grounding = [
    {
        "id": r["chunk_id"],
        "source": r["title"],
        "text": r["chunk"],
        "score": r["@search.score"],
    }
    for r in results
]
