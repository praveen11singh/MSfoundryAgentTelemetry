# MS Foundry Agent Telemetry Samples

This repository contains sample Python scripts demonstrating how to implement telemetry tracing for agents in Azure AI Projects (Microsoft Foundry). The samples showcase different tracing configurations, including console output, Azure Monitor integration, and custom attributes.

## Prerequisites

- Python 3.8 or later
- An Azure account with access to Azure AI Projects
- Microsoft Foundry project set up

## Installation

Install the required dependencies:

```bash
pip install "azure-ai-projects>=2.0.0" python-dotenv opentelemetry-sdk azure-core-tracing-opentelemetry azure-monitor-opentelemetry
```

## Environment Variables

Set the following environment variables before running the samples:

- `FOUNDRY_PROJECT_ENDPOINT`: The Azure AI Project endpoint from your Microsoft Foundry portal.
- `FOUNDRY_MODEL_NAME`: The deployment name of the AI model from the "Models + endpoints" tab.
- `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING`: Set to `true` to enable GenAI telemetry tracing.
- `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: Optional. Set to `true` to trace message content (may contain personal data).

## Samples

### 1. Basic Console Tracing (`agent_basic_with_console_tracing.py`)

Demonstrates basic agent operations with telemetry tracing output to the console.

**Usage:**
```bash
python agent_basic_with_console_tracing.py
```

### 2. Azure Monitor Tracing (`agent_azure_monitor_tracing.py`)

Shows how to integrate telemetry tracing with Azure Monitor for centralized logging and monitoring.

**Usage:**
```bash
python agent_azure_monitor_tracing.py
```

### 3. Custom Attributes Tracing (`agent_tracing_custom_attributes.py`)

Illustrates adding custom attributes to telemetry traces for enhanced observability.

**Usage:**
```bash
python agent_tracing_custom_attributes.py
```

## Contributing

Contributions are welcome! Please submit issues and pull requests.

## License

Copyright (c) Microsoft Corporation. Licensed under the MIT License.