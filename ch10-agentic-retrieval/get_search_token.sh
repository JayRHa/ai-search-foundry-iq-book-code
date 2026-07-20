#!/usr/bin/env bash
set -euo pipefail

# One token, scoped to the search service, reused across the calls below.
az account get-access-token \
  --scope https://search.azure.com/.default \
  --query accessToken -o tsv
