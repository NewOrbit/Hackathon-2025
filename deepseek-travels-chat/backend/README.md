```
uv pip install -r requirements.txt
uv run main.py
```

need a `.env` with:

```
AZURE_OPENAI_ENDPOINT=https://mkolo-mfxqosv8-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-5-nano/chat/completions?api-version=2025-01-01-preview
AZURE_OPENAI_API_KEY=
AZURE_API_VERSION=2024-12-01-preview
DEPLOYMENT_NAME=gpt-5-nano
ATTRACTIONS_MCP_URL=http://127.0.0.1:8008/mcp/
WEATHER_MCP_URL=http://127.0.0.1:8009/mcp/
TRAVEL_REQUIREMENTS_MCP_URL=http://127.0.0.1:8010/mcp/
BOOKING_MCP_URL=http://127.0.0.1:8011/mcp/
```

then `POST localhost:8000/chat`

```
{
    "message": "Hello! I am going to Skegness for two weeks. I have a 20L rucksack. I am going skydiving."
}
```