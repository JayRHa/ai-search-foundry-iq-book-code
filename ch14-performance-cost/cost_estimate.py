# Rough monthly cost model for an AI-enabled Azure AI Search workload.
# All rates are mid-2026 US approximations — verify on the pricing calculator.

# --- Corpus and workload assumptions ---
chunks              = 2_000_000
dims                = 1_536          # text-embedding-3-large truncated via MRL
bytes_per_dim       = 1              # scalar quantization -> int8 (1 byte)
avg_tokens_per_chunk = 500
monthly_queries     = 3_000_000
monthly_refresh_pct = 0.05
query_tokens        = 20             # per user question, embedded at query time

# --- Rates (USD, approximate) ---
embed_per_mtok      = 0.13           # text-embedding-3-large
semantic_per_1k     = 1.00           # semantic ranker, first 1k/month free
s1_su_month         = 245.0          # S1 per search unit per month

# --- Vector memory sizing (drives tier/partition choice) ---
raw_gb   = chunks * dims * bytes_per_dim / 1e9
vec_gb   = raw_gb * 1.05 * 1.10       # ~5% HNSW overhead, ~10% deletes
# S1 partition = 35 GB vector quota; how many partitions do we need?
import math
partitions = max(1, math.ceil(vec_gb / 35))
replicas   = 2                        # 2 replicas -> query SLA + headroom for 5 QPS
search_units = partitions * replicas
compute_cost = search_units * s1_su_month

# --- Embedding at index time (initial + monthly refresh) ---
initial_embed = chunks * avg_tokens_per_chunk / 1e6 * embed_per_mtok
monthly_embed_index = initial_embed * monthly_refresh_pct

# --- Embedding at query time ---
monthly_embed_query = monthly_queries * query_tokens / 1e6 * embed_per_mtok

# --- Semantic ranker (per query, first 1k free) ---
billable_semantic = max(0, monthly_queries - 1_000)
semantic_cost = billable_semantic / 1_000 * semantic_per_1k

print(f"Vector memory needed:     {vec_gb:6.1f} GB")
print(f"Config: {partitions}P x {replicas}R = {search_units} SU")
print(f"Compute (S1, {search_units} SU):   ${compute_cost:9,.0f}/mo")
print(f"Embedding at index time:  ${monthly_embed_index:9,.2f}/mo (+ ${initial_embed:,.0f} one-time)")
print(f"Embedding at query time:  ${monthly_embed_query:9,.2f}/mo")
print(f"Semantic ranker:          ${semantic_cost:9,.0f}/mo")
print(f"---")
print(f"Monthly total:            "
      f"${compute_cost + monthly_embed_index + monthly_embed_query + semantic_cost:,.0f}")
