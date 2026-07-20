#!/usr/bin/env bash
set -euo pipefail

# Let the search service READ blobs it indexes (no storage account key).
az role assignment create \
  --assignee "<search-service-managed-identity-object-id>" \
  --role "Storage Blob Data Reader" \
  --scope "/subscriptions/<sub>/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/mydata"

# Let the search service CALL the embedding model for integrated vectorization.
az role assignment create \
  --assignee "<search-service-managed-identity-object-id>" \
  --role "Cognitive Services OpenAI User" \
  --scope "/subscriptions/<sub>/resourceGroups/rg-ai/providers/Microsoft.CognitiveServices/accounts/my-aoai"
