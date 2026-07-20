#!/usr/bin/env bash
set -euo pipefail

# Allow Entra ID (RBAC) auth on the data plane, and turn OFF API keys entirely
az search service update \
  --name my-search-book \
  --resource-group rg-search-book \
  --aad-auth-failure-mode http403 \
  --auth-options aadOrApiKey

# Once every client uses RBAC, disable local (key) auth completely:
az resource update \
  --ids $(az search service show -n my-search-book -g rg-search-book --query id -o tsv) \
  --set properties.disableLocalAuth=true
