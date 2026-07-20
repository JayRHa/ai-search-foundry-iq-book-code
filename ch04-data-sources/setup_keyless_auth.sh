#!/usr/bin/env bash
set -euo pipefail

# Give the search service a system-assigned managed identity, then grant it
# read-only data access to the storage account it will index.

# Give the search service a system-assigned managed identity.
az search service update \
  --name my-search-service \
  --resource-group rg-knowledge \
  --identity-type SystemAssigned

# Grant the search service's identity read-only data access to the storage account.
SEARCH_MI_PRINCIPAL_ID="<principal-id-from-previous-step>"
STORAGE_ID=$(az storage account show \
  --name mystorageacct --resource-group rg-knowledge --query id -o tsv)

az role assignment create \
  --assignee "$SEARCH_MI_PRINCIPAL_ID" \
  --role "Storage Blob Data Reader" \
  --scope "$STORAGE_ID"
