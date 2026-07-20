import os
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType,
    SimpleField, SearchableField,
)

endpoint = os.environ["SEARCH_ENDPOINT"]   # https://my-search-book.search.windows.net
credential = DefaultAzureCredential()       # no key, uses your az login identity

index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="title", type=SearchFieldDataType.String),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SimpleField(name="category", type=SearchFieldDataType.String,
                filterable=True, facetable=True),
]

index = SearchIndex(name="hello-index", fields=fields)
result = index_client.create_or_update_index(index)
print(f"Created index: {result.name}")
