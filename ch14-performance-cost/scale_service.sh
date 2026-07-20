#!/usr/bin/env bash
set -euo pipefail

# Scale UP for a large reindexing job: more partitions for indexing throughput,
# and enough replicas to keep serving queries while it runs.
az search service update \
  --name my-search-service \
  --resource-group rg-knowledge \
  --partition-count 3 \
  --replica-count 2

# ...run the reindex, then scale partitions back DOWN for steady-state serving.
az search service update \
  --name my-search-service \
  --resource-group rg-knowledge \
  --partition-count 1 \
  --replica-count 2
