# API Documentation

## APIs Served by This Project

### Endpoints

#### GET /state
- **Method and Path:** GET /state
- **Description:** Returns the current graph state for a given thread ID.
- **Request:**
  - Headers: None specific
  - Query Parameters:
    - `thread_id` (string, required): The thread identifier for which to fetch the state.
- **Response:**
  - Success: JSON object representing the formatted state snapshot.
  - Error: HTTP 400 if `thread_id` is missing, with error detail.
- **Authentication:** None explicitly required; CORS allows all origins.
- **Example:**
  ```
  GET /state?thread_id=abc123
  Response: 200 OK
  {
    ...formatted state snapshot JSON...
  }
  ```

#### POST /agent (proxied via Next.js backend)
- **Method and Path:** POST /agent (proxied through Next.js route at `/client/app/api/agent/route.ts`)
- **Description:** Proxy endpoint forwarding requests to the AI agent service `/agent` endpoint. Used to prevent exposing the AI service publicly and to avoid client-side authentication complexity.
- **Request:**
  - Headers:
    - `Content-Type: application/json`
    - `Accept: text/event-stream`
    - `x-tenant-id`: fixed tenant ID string
  - Body: JSON payload forwarded to the AI agent service.
- **Response:**
  - Success: Streams server-sent events (SSE) from the AI agent service.
  - Error: JSON error message with status 500 if proxying fails.
- **Authentication:** None on proxy itself; relies on internal network security.
- **Example:**
  ```
  POST /api/agent
  Body: { ...agent request JSON... }
  Response: text/event-stream (SSE)
  ```

### Authentication & Security
- No explicit authentication on the FastAPI `/state` endpoint.
- CORS middleware allows all origins, methods, and headers (should be restricted in production).
- Proxy endpoint in Next.js hides the AI agent service from public exposure.
- Environment variables (e.g., `OPENWEATHER_API_KEY`) used for external API authentication.
- Ethical and security guidelines emphasize user consent, data privacy, and access control.

### Rate Limiting & Constraints
- No explicit rate limiting or throttling observed in the code.
- Resilience patterns include error handling in proxy and external API calls.
- SSE used for streaming responses to clients.

## External API Dependencies

### Services Consumed

#### OpenWeather API
- **Service Name & Purpose:** OpenWeather API for fetching current weather data.
- **Base URL/Configuration:** `https://api.openweathermap.org/data/2.5/weather`
- **Endpoints Used:** `/weather?lat={latitude}&lon={longitude}&appid={API_KEY}`
- **Authentication Method:** API key passed as query parameter (`appid`).
- **Error Handling:** Checks HTTP response status; logs error code if not 200.
- **Retry/Circuit Breaker Configuration:** None observed; simple synchronous HTTP request via `requests.get`.

### Integration Patterns
- The project uses a microservice-like pattern with a FastAPI backend serving state and a Next.js frontend proxying AI agent requests.
- SSE (Server-Sent Events) used for streaming real-time updates to clients.
- External API calls (OpenWeather) are integrated synchronously within async functions.
- Tools and commands are defined as async functions decorated with `@tool` for modular AI capabilities.
- Proxy pattern in Next.js backend to secure AI agent service and handle streaming responses.

## Available Documentation
- `README.md` provides an overview of the project, technology stack, installation instructions, current and future capabilities, and security guidelines.
- No explicit OpenAPI or GraphQL schema files found.
- Code comments provide inline documentation for key functions and endpoints.
- Documentation quality is moderate; README is clear but API details are mostly inferred from code.

---

This documentation summarizes the implemented APIs, external dependencies, and integration patterns for the IcalAI project. It is intended to assist developers in understanding and integrating with the service effectively.