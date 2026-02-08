# Code Structure Analysis

## Architectural Overview
The project "IcalAI" is an AI-powered digital clone agent designed to mimic user voice and personality for natural, personalized interactions. It is built primarily using Python with FastAPI as the web framework for API development. The system leverages AI models such as OpenAI's GPT and Whisper, LangChain, and LangGraph frameworks for language and graph-based AI processing. The architecture is modular, separating client-side UI components (React/Next.js) and server-side AI agent logic and API services. The backend uses asynchronous programming with asyncio and integrates with PostgreSQL for state checkpointing and Redis (planned) for async task handling. The system is designed with extensibility in mind, supporting multiple AI tools and external microservices (MCP servers).

## Core Components
- **Client (React/Next.js)**: Contains UI components, hooks, and pages for chat, agent interaction, and theming. Organized under `/client` with subdirectories for components, hooks, and API routes.
- **Server (FastAPI Python)**: Hosts the API endpoints and agent logic under `/server`. Key files include:
  - `server.py`: Main FastAPI app with endpoints for agent control, state retrieval, and event streaming.
  - `agent/graph.py`: Defines AI tools, state models, and asynchronous tool invocation logic.
  - `agent/graph_builder.py`: Builds and compiles the AI agent graph, defines tools and prompts.
  - `agent/prompts.py`: Contains prompt templates for the AI agent system.
- **Third Parties**: Contains integrations such as text-to-speech under `/third_parties`.

## Service Definitions
- **FastAPI Service (`server.py`)**: Provides REST endpoints for:
  - `/state`: Retrieve current graph state.
  - `/history`: Retrieve full state history.
  - `/agent`: Start, resume, fork, or replay agent execution with streaming event responses.
  - `/agent/stop`: Stop running agent threads.
- **Agent Tools (in `agent/graph.py` and `graph_builder.py`)**: Asynchronous functions representing AI tools like weather lookup, reminders, calendar checks, email writing, and meeting scheduling.
- **Graph Compilation and Execution**: The agent graph is compiled and executed with checkpointing support via PostgreSQL, enabling state persistence and recovery.

## Interface Contracts
- **TypedDicts and Pydantic Models**: Used extensively to define structured data contracts for tool inputs, state representations, and API request/response payloads.
- **Tool Interface**: Tools are defined as async functions decorated with `@tool` that accept typed inputs and return structured messages.
- **Event Streaming**: The server streams events to clients using Server-Sent Events (SSE) with structured event types (debug, messages, custom).

## Design Patterns Identified
- **Hexagonal Architecture**: Clear separation between domain logic (agent tools, graph building) and infrastructure (API, database checkpointing).
- **Event-Driven Architecture**: Use of async event streams for real-time agent interaction.
- **Dependency Injection**: Use of configuration objects and dependency passing (e.g., checkpointer) to decouple components.
- **Decorator Pattern**: `@tool` decorator to mark AI tool functions.
- **State Management**: Use of state graphs and checkpointing for managing AI agent state transitions.

## Component Relationships
- The **FastAPI server** acts as the entry point, exposing REST and SSE endpoints.
- The server uses the **agent graph builder** to compile AI agent graphs with tools and prompts.
- The **agent graph** executes asynchronously, invoking tools and updating state.
- State is persisted and restored via **PostgreSQL checkpointing**.
- The **client** interacts with the server API and streams events to provide a responsive UI.
- External MCP servers and third-party services can be integrated as tools.

## Key Methods & Functions
- `server.py`:
  - `state()`: Returns current graph state.
  - `history()`: Returns full state history.
  - `agent()`: Handles agent lifecycle commands (run, resume, fork, replay) and streams events.
  - `stop_agent()`: Stops running agent threads.
- `agent/graph.py`:
  - `weather_tool()`, `create_reminder_tool()`, `check_calendar_availability_tool()`: Example AI tools.
  - `chatbot()`: Main chatbot tool invoking LLM with bound tools.
- `agent/graph_builder.py`:
  - `create_prompt()`: Constructs system prompt for the agent.
  - Various tool functions like `write_email()`, `schedule_meeting()`.
- `agent/prompts.py`:
  - `agent_system_prompt`: Template for agent system prompt.
  - `agent_system_prompt_memory`: Extended prompt with memory management instructions.

## Available Documentation
- `README.md` at project root: Provides an introduction, technology stack, and installation instructions. Quality is basic but informative.
- `.ai/docs/README.md`: Not found (file missing or path incorrect).
- `.env.example`: Lists environment variables needed for API keys.
- Code is well-commented with docstrings explaining key functions and classes.

Overall, the codebase is organized with a clear separation of concerns between client UI, server API, and AI agent logic. It uses modern async Python patterns and AI frameworks to build a modular, extensible digital assistant system. The architecture supports real-time interaction, state persistence, and integration with external tools and services.