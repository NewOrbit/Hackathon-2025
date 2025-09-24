
## Setup

1. Install Claud Desktop: https://claude.ai/download
2. Add `claude_desktop_config.json` file in install folder (likely `C:\Users\<your-username>\AppData\Local\AnthropicClaude`) with the following contents (replace folder location):

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["C:\\<path-to-repo>\\Hackathon-2025\\src\\mcp\\movie-reviews-mcp\build\\index.js"]
    }
  }
}
```
