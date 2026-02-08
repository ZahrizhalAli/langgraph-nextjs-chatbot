import json
import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
except Exception:  # pragma: no cover - optional dependency
    MultiServerMCPClient = None


# MCP server configuration can be provided as JSON in MCP_SERVERS_JSON.
# Example:
# MCP_SERVERS_JSON='{"calendar":{"transport":"sse","url":"http://localhost:3002/sse"}}'
def _load_mcp_servers() -> Dict[str, Dict[str, Any]]:
    raw = os.getenv("MCP_SERVERS_JSON", "").strip()
    if not raw:
        return {}
    try:
        servers = json.loads(raw)
        if not isinstance(servers, dict):
            raise ValueError("MCP_SERVERS_JSON must be a JSON object")
        return servers
    except Exception as exc:
        logger.warning("Invalid MCP_SERVERS_JSON: %s", exc)
        return {}


class MCPToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Any] = {}
        self._loaded = False

    async def load_tools(self) -> List[Any]:
        if self._loaded:
            return list(self._tools.values())

        if MultiServerMCPClient is None:
            logger.info("langchain-mcp-adapters is not installed; skipping MCP tool load.")
            self._loaded = True
            return []

        servers = _load_mcp_servers()
        if not servers:
            self._loaded = True
            return []

        try:
            client = MultiServerMCPClient(servers)
            tools = await client.get_tools()
            self._tools = {tool.name: tool for tool in tools}
        except Exception as exc:
            logger.warning("Failed to load MCP tools: %s", exc)
            self._tools = {}
        finally:
            self._loaded = True

        return list(self._tools.values())

    def get_tool(self, name: str) -> Any | None:
        return self._tools.get(name)

    def tool_names(self) -> set[str]:
        return set(self._tools.keys())


MCP_TOOL_REGISTRY = MCPToolRegistry()
