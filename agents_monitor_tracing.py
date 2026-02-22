import asyncio
import time
from azure.ai.projects.aio import AIProjectClient
from azure.ai.agents.models import ListSortOrder, MessageTextContent
from azure.identity.aio import DefaultAzureCredential
from opentelemetry import trace
import os
from azure.monitor.opentelemetry import configure_azure_monitor

from dotenv import load_dotenv

load_dotenv()

scenario = os.path.basename(__file__)
tracer = trace.get_tracer(__name__)


async def main() -> None:

    async with DefaultAzureCredential() as creds:
        async with AIProjectClient(
            endpoint=os.environ["PROJECT_ENDPOINT"],
            credential=creds,
        ) as project_client:

            async with project_client:
                agents_client = project_client.agents

                # Enable Azure Monitor tracing
                application_insights_connection_string = os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
                configure_azure_monitor(connection_string=application_insights_connection_string)

                with tracer.start_as_current_span(scenario):
                    async with agents_client:
                        agent = await agents_client.create_agent(
                            model=os.environ["MODEL_DEPLOYMENT_NAME"],
                            name="pk-agent-appinsights-tracing",
                            instructions="You are helpful agent",
                        )
                        print(f"Created agent, agent ID: {agent.id}")

                        thread = await agents_client.threads.create()
                        print(f"Created thread, thread ID: {thread.id}")

                        message = await agents_client.messages.create(
                            thread_id=thread.id, role="user", content="Hello, tell me a joke"
                        )
                        print(f"Created message, message ID: {message.id}")

                        run = await agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
                        print(f"Run completed with status: {run.status}")

                        # await agents_client.delete_agent(agent.id)
                        # print("Deleted agent")

                        messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
                        async for msg in messages:
                            last_part = msg.content[-1]
                            if isinstance(last_part, MessageTextContent):
                                print(f"{msg.role}: {last_part.text.value}")


if __name__ == "__main__":
    asyncio.run(main())