# Datastore MCP Server

Persistent, token-efficient, namespaced key-value storage for MCP agents.

## Features
- Namespaces to segment data logically
- Arbitrary (MessagePack-serializable) values: primitives, lists, dicts, small vectors
- Metadata per record (e.g., source, tags)
- Incrementing revisions per key
- Append-only journal + compact snapshot for durability
- Tools for CRUD + dump + stats + compaction
- Resource URIs for quick retrieval: `memory://{namespace}/{key}` and `memory://{namespace}`
- Prompt helper to summarize a namespace subset

## File Format
- Snapshot (`store.snapshot.msgpack`): msgpack map `{ namespace -> { key -> {"v": value, "t": ts, "rev": int, "m"?: metadata} } }`
- Journal (`store.journal.msgpack`): sequence of msgpack objects:
  - Write: `{"op":1,"ns":str,"k":str,"v":any,"t":int,"m"?:dict,"rev":int}`
  - Delete: `{"op":0,"ns":str,"k":str,"rev":int}`

Short property names reduce serialized size and improve token efficiency if later surfaced to an LLM.

## Tools
| Tool | Description |
|------|-------------|
| `save_data(key, data, namespace='default', metadata=None, replace=True)` | Store/replace a value |
| `read_data(key, namespace='default')` | Retrieve one record |
| `list_keys(namespace='default')` | List keys in a namespace |
| `delete_data(key, namespace='default')` | Remove a key |
| `dump_namespace(namespace='default', limit=None, include_metadata=False)` | Bulk read subset |
| `compact_store()` | Rewrite snapshot & clear journal |
| `stats()` | Storage statistics |

## Resources
- `memory://{namespace}/{key}` → compact JSON single record
- `memory://{namespace}` → namespace summary (keys truncated to 50)

## Prompt
`memory_summary_prompt(namespace='default', objective=None, limit=10)` returns a concise textual overview helpful for grounding a model.

## Example Flow
```python
# Save
save_data(key="conversation_1", data={"messages": ["hi", "hello"], "summary": "greeting"})
# Read
read_data(key="conversation_1")
# List
list_keys(namespace="default")
# Dump first 5
dump_namespace(limit=5)
# Compact
compact_store()
# Stats
stats()
```

## Token Efficiency Notes
- MessagePack avoids verbose JSON quoting; internal management uses very short keys.
- Use `dump_namespace` with a limit for summarization; avoid asking the model to ingest the entire store.
- Metadata is optional—omit when not necessary.
- Store embeddings or large blobs sparingly; consider external vector DB for high-dimensional data.

## Compaction Strategy
- Journal is append-only for durability.
- Call `compact_store` occasionally (e.g., after N writes) to reduce disk size and replay time.

## Future Enhancements (ideas)
- Optional zstd compression layer
- TTL / expiration per record
- File-lock for multi-process safety
- Query by metadata indexes

## Running
From this directory:
```
uv run mcp dev main.py
```

## License
Internal hackathon component; adapt as needed.
