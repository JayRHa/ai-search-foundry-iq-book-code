# Continues from create_grounded_agent.py — reuses the `project` client and
# the created `agent`. Ask a question and print the answer with citations.

# Get an OpenAI-shaped client from the project and call the agent.
client = project.get_openai_client()

response = client.responses.create(
    input="What does our travel policy say about booking rail versus air?",
    # 'required' forces retrieval for this single-purpose knowledge agent.
    tool_choice="required",
    extra_body={
        "agent_reference": {"name": agent.name, "type": "agent_reference"}
    },
)

# Print the answer, then walk the annotations to surface the citations.
for item in response.output:
    for content in getattr(item, "content", []):
        if getattr(content, "text", None):
            print(content.text)
        for ann in getattr(content, "annotations", []):
            if ann.type == "url_citation":
                print(f"  ↳ cited: {ann.url}")
