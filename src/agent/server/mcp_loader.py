from __future__ import annotations

import asyncio
import os
from typing import Dict, List, Tuple

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection

MCP_CONFIG: Tuple[Tuple[str, str, str], ...] = (
    ("attractions", "ATTRACTIONS_MCP_URL", "http://127.0.0.1:8008/mcp/"),
    ("weather", "WEATHER_MCP_URL", "http://127.0.0.1:8009/mcp/"),
    ("macros", "MACROS_MCP_URL", "http://127.0.0.1:8010/mcp/"),
    ("nutrition_plan", "NUTRITION_PLAN_MCP_URL", "http://127.0.0.1:8011/mcp/"),
    ("trivia", "TRIVIA_MCP_URL", "http://127.0.0.1:8012/mcp/"),
)


def _build_connections() -> Tuple[Dict[str, StreamableHttpConnection], List[str]]:
    connections: Dict[str, StreamableHttpConnection] = {}
    notes: List[str] = []
    for name, env_key, default in MCP_CONFIG:
        url = os.getenv(env_key, default)
        if not url:
            continue
        connections[name] = StreamableHttpConnection(transport="streamable_http", url=url)
        notes.append(f"[{name}] {url}")
    return connections, notes


async def _load_tools_async(connections: Dict[str, StreamableHttpConnection], notes: List[str]):
    client = MultiServerMCPClient(connections)
    collected = []
    descriptions = list(notes)

    for server_name in connections.keys():
        try:
            tools = await client.get_tools(server_name=server_name)
            collected.extend(tools)
            for tool in tools:
                desc = tool.description or ""
                label = f"{server_name}:{tool.name}"
                descriptions.append(f"{label} - {desc}" if desc else label)
        except Exception as exc:  # noqa: BLE001
            descriptions.append(f"{server_name} (failed: {exc})")

    return collected, descriptions


def load_mcp_tools_sync() -> Tuple[List, List[str]]:
    connections, notes = _build_connections()
    if not connections:
        return [], notes

    try:
        return asyncio.run(_load_tools_async(connections, notes))
    except RuntimeError:
        # Already inside an event loop (e.g. notebook); create a new loop
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(_load_tools_async(connections, notes))
        finally:
            loop.close()
            asyncio.set_event_loop(None)


