"""Datastore MCP Server - Persistent token-efficient namespaced key-value storage.

Run:
    uv run mcp dev main.py
"""
from typing import Any, Dict, Optional
import json
import os

from mcp.server.fastmcp import FastMCP

from storage import DataStore

DATA_DIR = os.path.join(os.path.dirname(__file__), ".data")

datastore = DataStore(DATA_DIR)

mcp = FastMCP("Datastore", port=8012)

# -------------------- Tools --------------------
@mcp.tool()
def save_data(key: str, data: Any, namespace: str = "default", metadata: Optional[Dict[str, Any]] = None, replace: bool = True) -> Dict[str, Any]:
    """Save a value under a namespaced key.

    Args:
        key: Identifier within namespace.
        data: Any JSON-serializable / msgpack-serializable value.
        namespace: Logical grouping (default 'default').
        metadata: Optional small dict for context.
        replace: If False and key exists, returns error.
    """
    return datastore.save(key, data, namespace, metadata, replace)


@mcp.tool()
def read_data(key: str, namespace: str = "default") -> Dict[str, Any]:
    """Read a stored record."""
    return datastore.read(key, namespace)


@mcp.tool()
def list_keys(namespace: str = "default") -> Dict[str, Any]:
    """List keys in a namespace."""
    return datastore.list_keys(namespace)


@mcp.tool()
def delete_data(key: str, namespace: str = "default") -> Dict[str, Any]:
    """Delete a key from a namespace."""
    return datastore.delete(key, namespace)


@mcp.tool()
def dump_namespace(namespace: str = "default", limit: Optional[int] = None, include_metadata: bool = False) -> Dict[str, Any]:
    """Return multiple items from a namespace.

    Args:
        namespace: Namespace name
        limit: Max number of items (None = all)
        include_metadata: Include metadata if available
    """
    return datastore.dump_namespace(namespace, limit, include_metadata)


@mcp.tool()
def compact_store() -> Dict[str, Any]:
    """Force compaction (rewrite snapshot & clear journal)."""
    return datastore.compact()


@mcp.tool()
def stats() -> Dict[str, Any]:
    """Return datastore statistics."""
    return datastore.stats()

# -------------------- Resources --------------------
@mcp.resource("memory://{namespace}/{key}")
def memory_key_resource(namespace: str, key: str) -> str:
    rec = datastore.read(key, namespace)
    if "error" in rec:
        return f"Memory entry not found: {namespace}/{key}\n"
    # Compact JSON representation
    payload = {"ns": namespace, "k": key, "v": rec.get("value"), "t": rec.get("timestamp"), "rev": rec.get("rev")}
    if "metadata" in rec:
        payload["m"] = rec["metadata"]
    return json.dumps(payload, separators=(",", ":"))


@mcp.resource("memory://{namespace}")
def memory_namespace_resource(namespace: str) -> str:
    listing = datastore.list_keys(namespace)
    keys = listing.get("keys", [])
    summary = {"namespace": namespace, "count": listing.get("count", 0), "keys": keys[:50]}
    return json.dumps(summary, separators=(",", ":"))

# -------------------- Prompt --------------------
@mcp.prompt()
def memory_summary_prompt(namespace: str = "default", objective: Optional[str] = None, limit: int = 10) -> str:
    dump = datastore.dump_namespace(namespace, limit)
    lines = []
    if objective:
        lines.append(f"Objective: {objective}")
    lines.append(f"Namespace '{namespace}' sample (limit={limit}):")
    for item in dump.get("items", []):
        val = item.get("value")
        # Truncate long string values for prompt friendliness
        if isinstance(val, str) and len(val) > 200:
            val = val[:197] + "..."
        lines.append(f"- {item['key']}: {val}")
    lines.append("Use these stored items as context; retrieve more with tools if needed.")
    return "\n".join(lines)

@mcp.prompt()
def retrieve_data_prompt(
    user_request: str,
    namespace: str = "default",
    today_iso: Optional[str] = None
) -> str:
    """
    Guide the model to decide which datastore operations to perform
    to satisfy a retrieval-style user request (e.g., 'today's meal plan').

    user_request: The original natural language query from the user.
    namespace: Namespace to inspect.
    today_iso: Pass in today's date (YYYY-MM-DD) so the model doesn't hallucinate.
    strategy: Retrieval heuristic name (future extension).
    """
    listing = datastore.list_keys(namespace)
    keys = listing.get("keys", [])
    lines = []
    lines.append("You are planning data retrieval from a persistent key-value store.")
    lines.append(f"User request: {user_request}")
    if today_iso:
        lines.append(f"Today's date (ISO): {today_iso}")
    lines.append(f"Namespace: {namespace}")
    lines.append(f"Available key count: {listing.get('count', 0)}")
    # Show a limited slice only (avoid huge prompt)
    preview = keys[:100]
    lines.append("Keys:")
    for k in preview:
        lines.append(f"- {k}")
    if len(keys) > len(preview):
        lines.append(f"... ({len(keys) - len(preview)} more not shown)")
    lines.append("")
    lines.append("Retrieval Guidelines:")
    lines.append("1. Derive candidate key names from the user request (e.g., date-based).")
    lines.append("2. If an exact key match exists, plan to call: read_data(key=<key>, namespace=<namespace>).")
    lines.append("3. If multiple partial matches (e.g. all keys containing today's date), pick the most specific; if unsure, call dump_namespace with a limit.")
    lines.append("4. If NO relevant key, respond with PLAN:NOT_FOUND (do not fabricate data).")
    lines.append("5. Do NOT invent keys; only use keys listed above.")
    lines.append("")
    lines.append("Respond ONLY with a PLAN block in one of these forms:")
    lines.append("PLAN:READ key=<existing_key> namespace=<namespace>")
    lines.append("PLAN:DUMP namespace=<namespace> limit=<=20")
    lines.append("PLAN:NOT_FOUND")
    lines.append("")
    lines.append("Do not include any other explanatory text.")
    return '\\n'.join(lines)

if __name__ == "__main__":
    mcp.run("streamable-http")
