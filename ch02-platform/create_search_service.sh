#!/usr/bin/env bash
set -euo pipefail

# Log in with your own identity (this is also what makes keyless auth work later)
az login

# Create the resource group and the search service
az group create \
  --name rg-search-book \
  --location swedencentral

az search service create \
  --name my-search-book \
  --resource-group rg-search-book \
  --location swedencentral \
  --sku basic \
  --partition-count 1 \
  --replica-count 1
