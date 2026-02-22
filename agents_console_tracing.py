import asyncio
import time
import sys
from azure.core.settings import settings

settings.tracing_implementation = "opentelemetry"
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from azure.ai.projects.aio import AIProjectClient
from azure.ai.agents.models import ListSortOrder, MessageTextContent
from azure.identity.aio import DefaultAzureCredential
from opentelemetry import trace
import os
from azure.ai.agents.telemetry import AIAgentsInstrumentor

# Setup tracing to console
# Requires opentelemetry-sdk
span_exporter = ConsoleSpanExporter()
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)

AIAgentsInstrumentor().instrument()

scenario = os.path.basename(__file__)
tracer = trace.get_tracer(__name__)


@tracer.start_as_current_span(__file__)
async def main() -> None:

    async with DefaultAzureCredential() as creds:
        async with AIProjectClient(
            endpoint=os.environ["PROJECT_ENDPOINT"],
            credential=creds,
        ) as project_client:

            async with project_client:
                agents_client = project_client.agents

                agent = await agents_client.create_agent(
                    model=os.environ["MODEL_DEPLOYMENT_NAME"], name="my-agent", instructions="You are helpful agent"
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

                await agents_client.delete_agent(agent.id)
                print("Deleted agent")

                messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
                async for msg in messages:
                    last_part = msg.content[-1]
                    if isinstance(last_part, MessageTextContent):
                        print(f"{msg.role}: {last_part.text.value}")


if __name__ == "__main__":
    asyncio.run(main())