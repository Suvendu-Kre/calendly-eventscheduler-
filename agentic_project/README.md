# Agentic Project

This project implements an AI agent using the Langchain framework.

## Overview

The agent is designed to automate tasks based on user input, leveraging configured tools and a defined workflow.

## Architecture

The project follows a modular structure:

-   **config/:** Contains configuration files (e.g., agent settings, API keys).
-   **data/:** Stores data sources, memory (long-term and short-term), and tool-specific data.
-   **agents/:** Implements the main agent class and its core logic.
-   **tools/:** Defines the tools the agent can use.
-   **workflows/:** Defines the agent's workflow.
-   **observability/:** Provides logging, metrics, and tracing capabilities.
-   **guardrails/:** Implements input/output validation and content filtering.
-   **error\_handling/:** Handles errors with retry logic and circuit breakers.
-   **gcp/:** Contains deployment utilities for Google Cloud Platform.
-   **github/:** Includes CI/CD workflows for GitHub Actions.
-   **tests/:** Contains unit tests.

## Getting Started

1.  **Clone the repository:**


2.  **Set up the environment:**

    *   Run the appropriate setup script for your operating system:

        *   Windows: `setup.bat`
        *   Linux/macOS: `bash setup.sh`

    *   This will create a virtual environment, activate it, and install the required dependencies.

3.  **Configure environment variables:**

    *   Copy `.env.example` to `.env` and fill in your credentials (e.g., GCP credentials, API keys).

4.  **Run the application:**


    The application will start a FastAPI server.

## API Endpoints

-   **GET /health:** Health check endpoint.
-   **POST /chat:** Chat endpoint that accepts a JSON payload with a `message` field and returns a JSON payload with a `response` field.

## Configuration

The agent is configured using the `config/config.yaml` file.  This file defines the agent's name, system prompt, memory settings, security settings, error handling settings, and other parameters.

## Tools

The agent uses tools defined in the `tools/tool_manager.py` file.  These tools provide the agent with the ability to perform specific tasks, such as calculations or API calls.

## Observability

The project includes observability features using the `observability/monitoring.py` file.  This file defines decorators for logging request information and handling errors.

## Guardrails

The project includes guardrails for input and output validation using the `guardrails/safety.py` file.  This file defines functions for validating input and output to ensure they meet certain criteria.

## Error Handling

The project includes error handling with retry logic and circuit breakers using the `error_handling/handler.py` file.  This file defines functions for retrying failed operations and preventing cascading failures.

## Deployment

The project can be deployed to Google Cloud Platform using the utilities in the `gcp/deploy.py` file.  The project also includes CI/CD workflows for GitHub Actions in the `github/workflows/` directory.

## Testing

The project includes unit tests in the `tests/test_agent.py` file.  These tests can be run using pytest.