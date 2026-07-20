#!/usr/bin/env bash
set -euo pipefail

# Grant a principal the data-plane query role, scoped to one search service.
az role assignment create \
  --assignee "<principal-object-id>" \
  --role "Search Index Data Reader" \
  --scope "/subscriptions/<sub>/resourceGroups/rg-knowledge/providers/Microsoft.Search/searchServices/my-search-svc"
