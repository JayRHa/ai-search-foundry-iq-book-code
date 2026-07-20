from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from azure.identity import DefaultAzureCredential

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

kb_tool = MCPTool(
    server_label="knowledge-base",
    server_url=f"{SEARCH_ENDPOINT}/knowledgebases/support-kb/mcp?api-version=2026-05-01-preview",
    require_approval="never",
    allowed_tools=["knowledge_base_retrieve"],
    project_connection_id=CONNECTION_NAME,
)

agent = project.agents.create_version(
    agent_name="support-assistant",
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions=(
            "You are a support assistant. Use the knowledge base tool to answer every "
            "question. Never answer from your own knowledge. Cite the sources you use. "
            "If the knowledge base doesn't contain the answer, say 'I don't know'."
        ),
        tools=[kb_tool],
    ),
)
