#!/usr/bin/env bash
set -euo pipefail

SEARCH_ID=$(az search service show -n my-search-book -g rg-search-book --query id -o tsv)
ME=$(az ad signed-in-user show --query id -o tsv)

az role assignment create --assignee $ME \
  --role "Search Index Data Contributor" --scope $SEARCH_ID
az role assignment create --assignee $ME \
  --role "Search Index Data Reader" --scope $SEARCH_ID
