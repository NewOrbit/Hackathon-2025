"""MCP client builders for DeepseekTravels."""

from __future__ import annotations

import os
from typing import Any, Dict

from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv


DEFAULT_MCP_PORTS: Dict[str, int] = {
    "attractions": 8008,
    "weather": 8009,
    "requirements": 8010,
    "booking": 8011,
}


def _resolve_mcp_endpoint(env_var: str, server: str) -> str:
    value = os.getenv(env_var)
    if value:
        return value
    port = DEFAULT_MCP_PORTS.get(server)
    if port is None:
        raise ValueError(f"Unknown MCP server '{server}'")
    return f"http://localhost:{port}"


def build_mock_clients() -> dict[str, Any]:
    """Return MCP tool clients backed by the local mock MCP servers."""

    load_dotenv()

    if os.getenv("DEEPSEEKTRAVELS_USE_MOCKS", "true").lower() != "true":
        raise RuntimeError("Phase 1 requires mock mode enabled.")

    base_config: Dict[str, Dict[str, str]] = {
        "attractions": {
            "transport": "streamable_http",
            "url": _resolve_mcp_endpoint("ATTRACTIONS_MCP_URL", "attractions"),
        },
        "weather": {
            "transport": "streamable_http",
            "url": _resolve_mcp_endpoint("WEATHER_MCP_URL", "weather"),
        },
        "requirements": {
            "transport": "streamable_http",
            "url": _resolve_mcp_endpoint("REQUIREMENTS_MCP_URL", "requirements"),
        },
        "booking": {
            "transport": "streamable_http",
            "url": _resolve_mcp_endpoint("BOOKING_MCP_URL", "booking"),
        },
    }

    mcp_client = MultiServerMCPClient(base_config)

    return {
        "mcp_client": mcp_client,
        "mcp_config": base_config,
    }


__all__ = ["build_mock_clients"]

