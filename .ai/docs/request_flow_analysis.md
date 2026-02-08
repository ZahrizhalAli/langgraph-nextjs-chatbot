# Request Flow Analysis

## Entry Points Overview
The primary entry points for requests in the system are HTTP API endpoints exposed by a FastAPI application in the `server/server.py` file. These endpoints include:
- `GET /state`: Returns the current graph state for a given `thread_id`.
- `GET /history`: Returns the complete state history for a given `thread_id`.
- `POST /agent/stop`: Stops a running agent for a given `thread_id`.
- `POST /agent`: Runs or controls the agent with different request types (`run`, `resume`, `fork`, `replay`).

Additionally, there is a Next.js API route in `client/app/api/agent/route.ts` which acts as a proxy to the `/agent` endpoint of the backend API. This proxy is used to forward requests from the frontend to the backend securely.

## Request Routing Map
- FastAPI routes are defined in `server/server.py` using decorators such as `@app.get` and `@app.post`.
- The Next.js API route in `client/app/api/agent/route.ts` forwards POST requests to the backend `/agent` endpoint.
- The FastAPI app is run using `uvicorn` in the `main()` function within `server/server.py`.

## Middleware Pipeline
- The FastAPI app uses CORS middleware configured to allow all origins, credentials, methods, and headers.
- No other middleware components are explicitly defined in the provided code.
- The Next.js API route does not use middleware but handles streaming responses and error forwarding.

## Controller/Handler Analysis
- Handlers in `server/server.py` are async functions decorated with FastAPI route decorators.
- Each handler performs request validation (e.g., checking for required parameters like `thread_id` and `type`).
- The `/agent` POST handler processes different request types and manages an `active_connections` dictionary to track running agents.
- The `/agent` handler uses an async generator `generate_events` to stream events back to the client using Server-Sent Events (SSE).
- Utility functions in `server/utils.py` format various event types (`checkpoint_event`, `message_chunk_event`, `interrupt_event`, `custom_event`) for SSE streaming.
- The Next.js API route reads the streaming response from the backend and forwards it to the client, handling errors gracefully.

## Authentication & Authorization Flow
- No explicit authentication or authorization mechanisms are visible in the provided code.
- The Next.js API route includes a hardcoded header `"x-tenant-id"` which may be used for multi-tenant identification or authorization downstream, but no validation is shown.
- CORS middleware is permissive, allowing all origins.

## Error Handling Pathways
- FastAPI handlers raise `HTTPException` with appropriate status codes (400 for bad requests, 404 for not found).
- The `/agent` handler validates request body fields and raises errors for missing or invalid data.
- The Next.js API route checks the backend response status and throws errors if the response is not OK.
- Streaming errors in the Next.js API route are caught and an error event is written to the stream before closing.
- General errors in the Next.js API route return a JSON error response with status 500.

## Request Lifecycle Diagram
```
Client (Frontend)
   |
   | POST /api/agent (Next.js API Route)
   |------------------------------------>
   |                                    |
   |                            Proxy POST to /agent (FastAPI)
   |                                    |
   |                            Validate request body
   |                            Manage active_connections
   |                            Compile graph and stream events
   |                                    |
   |<-----------------------------------
   | Stream SSE events (checkpoint, messages, interrupts, custom)
   |
   | Forward SSE stream to client
   |
   V
Client (UI)

Other GET endpoints:
Client --> GET /state?thread_id=xxx --> Validate thread_id --> Fetch graph state --> Return JSON
Client --> GET /history?thread_id=xxx --> Validate thread_id --> Fetch state history --> Return JSON

POST /agent/stop:
Client --> POST /agent/stop with thread_id --> Validate thread_id --> Signal stop event --> Return status
```

This flow shows how requests enter through the frontend proxy or directly to the backend, are validated, processed by the LangGraph agent system, and streamed back to the client with real-time event updates. Error handling and request validation ensure robustness, while the middleware pipeline currently focuses on CORS configuration.