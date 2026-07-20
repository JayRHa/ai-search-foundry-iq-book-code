from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery, VectorizedQuery
from openai import AzureOpenAI

cred = DefaultAzureCredential()
client = SearchClient("https://<service>.search.windows.net", "kb-index", cred)

# Option A — service embeds the text (matches the index's vectorizer):
vq = VectorizableTextQuery(
    text="how do I get my laptop to stop overheating",
    k_nearest_neighbors=5,
    fields="text_vector",
)

results = client.search(
    vector_queries=[vq],
    select=["chunk_id", "title", "chunk"],
)
for r in results:
    print(round(r["@search.score"], 3), r["title"])

# Option B — embed it yourself, then send the raw vector.
# Must be the SAME model and dimensions used to build the index.
aoai = AzureOpenAI(azure_ad_token_provider=..., api_version="2024-10-21",
                   azure_endpoint="https://<aoai>.openai.azure.com")
embedding = aoai.embeddings.create(
    model="text-embedding-3-large",
    input="how do I get my laptop to stop overheating",
).data[0].embedding

raw_vq = VectorizedQuery(
    vector=embedding, k_nearest_neighbors=5, fields="text_vector",
)
results = client.search(vector_queries=[raw_vq], select=["title", "chunk"])
