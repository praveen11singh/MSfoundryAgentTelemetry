import os
from dotenv import load_dotenv

# [START imports_for_azure_monitor_tracing]
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor

# [END imports_for_azure_monitor_tracing]
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

agent = None

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=credential) as project_client,
):
  
    application_insights_connection_string = project_client.telemetry.get_application_insights_connection_string()
    configure_azure_monitor(connection_string=application_insights_connection_string)
   
    tracer = trace.get_tracer(__name__)
    scenario = os.path.basename(__file__)

    with tracer.start_as_current_span(scenario):
       
        with project_client.get_openai_client() as openai_client:
            agent_definition = PromptAgentDefinition(
                model=os.environ["FOUNDRY_MODEL_NAME"],
                instructions="You are a helpful assistant that answers general questions",
            )

            agent = project_client.agents.create_version(agent_name="MyAgent", definition=agent_definition)
            print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

            conversation = openai_client.conversations.create()
            print(f"Created conversation with initial user message (id: {conversation.id})")

            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "id": agent.id, "type": "agent_reference"}},
                input="What is the size of India in square miles?",
            )
            print(f"Response output: {response.output_text}")

            openai_client.conversations.delete(conversation_id=conversation.id)
            print("Conversation deleted")

    if agent:
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("Agent deleted")