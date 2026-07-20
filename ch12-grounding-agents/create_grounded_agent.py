import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    AzureAISearchTool,
    AzureAISearchToolResource,
    AISearchIndexResource,
    AzureAISearchQueryType,
)

# Keyless from the first line: DefaultAzureCredential resolves to your
# az-cli login locally, or the project's managed identity in Azure.
project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Resolve the connection you created in the project by NAME, not by a
# pasted resource id — the SDK hands you back the id.
search_conn = project.connections.get(os.environ["SEARCH_CONNECTION_NAME"])

# The tool: point it at ONE index, on that connection, with a query type.
# vector_semantic_hybrid = hybrid search + the semantic reranker (Ch. 9).
search_tool = AzureAISearchTool(
    azure_ai_search=AzureAISearchToolResource(
        indexes=[
            AISearchIndexResource(
                project_connection_id=search_conn.id,
                index_name=os.environ["SEARCH_INDEX_NAME"],
                query_type=AzureAISearchQueryType.VECTOR_SEMANTIC_HYBRID,
                top_k=5,
            )
        ]
    )
)

# Create the agent. The instructions do real work here: they tell the
# model to answer only from retrieved content and to always cite.
agent = project.agents.create_version(
    agent_name="knowledge-assistant",
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions=(
            "You answer questions about company policy and documentation. "
            "Answer ONLY from the Azure AI Search knowledge tool. If the "
            "tool returns nothing relevant, say you don't know — do not "
            "answer from general knowledge. Always cite your sources as "
            "[source]."
        ),
        tools=[search_tool],
    ),
)
print(f"Created agent: {agent.name}")
