#!/usr/bin/env bash
set -euo pipefail

# Disable admin/query keys entirely — the service accepts only Entra ID tokens.
az search service update \
  --name my-search-svc \
  --resource-group rg-knowledge \
  --disable-local-auth true
