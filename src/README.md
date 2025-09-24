# Hackathon-2025

This repository contains all materials for the hackathon focused on building agentic AI applications.

## Quick Links

There are 2 pre-built MCP servers and a Jupyter notebook that can be run to execute LangChain to communicate with these MCP servers.

- [Attractions MCP Server](mcp/attractions-mcp/README.md)
- [Weather MCP Server](mcp/weather-mcp/README.md)
- [Attractions Jupyter Notebook](agent/README.md)
- [Macros MCP Server](mcp/macros-mcp/README.md)
- [Nutritional Plan MCP Server](mcp/nutritional-plan-mcp/README.md)

## Getting Started

Follow these steps to set up and run Weather MCP/Attractions MCP service:

### Prerequisites

1. **Install Python 3.13**

   - Download from [python.org](https://www.python.org/downloads/)

2. **Install uv** (Python package manager)

   ```bash
   pip install uv
   ```

   **Windows users**: You may need to add the Python Scripts folder to your PATH environment variable:

   - If installed globally: `C:\Users\<your-username>\AppData\Local\Programs\Python\Python313\Scripts\`
   - If installed with `pip install --user uv`: `C:\Users\<your-username>\AppData\Roaming\Python\Python313\Scripts\`
   - Restart your command prompt/PowerShell after updating PATH

### Setup Steps

1. **Fork and clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Hackathon-2025
   ```

2. **Navigate to the weather-mcp or attractions-mcp directory**

   ```bash
   cd src/mcp/weather-mcp
   ```

   ```bash
   cd src/mcp/attractions-mcp
   ```

3. **Install dependencies**

   ```bash
   uv sync
   ```

4. **Run the MCP server**

   ```bash
   uv run mcp dev main.py
   ```

   The weather MCP service will start and a local UI will launch in the browser (MCP's have to be running to run the jupyter notebook).

   When using mcp dev you may need to change the support type dropdown to STDIO to use it.

> **⚠ Important Note:** If you are running the MCP to be consumed by the agent, do not run it in dev mode. Use the following command instead:
>
> ```bash
> uv run main.py
> ```

## Agent Notebook

Once your MCP services are running, you can explore the agent implementation in the Jupyter notebook:

- [Attractions Agent Notebook](agent/README.md)

## Creating a New MCP Service

To create your own MCP service, follow these steps:

1. **Navigate to the MCP folder**

   ```bash
   cd src/mcp
   ```

2. **Initialize a new MCP project**

   ```bash
   uv init mymcpname-mcp
   ```

3. **Add MCP dependencies**

   ```bash
   cd mymcpname-mcp
   uv add "mcp[cli]"
   ```

4. **Create your MCP service code**
   Update the `main.py` file with this default MCP code to get you started:

   ```python
   from mcp.server.fastmcp import FastMCP

   # Create an MCP server
   # you can add the port here so that it doesnt clash with other mcp servers
   mcp = FastMCP("myname")

   # Add an addition tool
   @mcp.tool()
   def add(a: int, b: int) -> int:
       """Add two numbers"""
       return a + b


   # Add a dynamic greeting resource
   @mcp.resource("greeting://{name}")
   def get_greeting(name: str) -> str:
       """Get a personalized greeting"""
       return f"Hello, {name}!"


   if __name__ == "__main__":
      mcp.run("streamable-http")
   ```

5. **Run your MCP service**

   ```bash
   uv run mcp dev main.py
   ```

6. **Start building your custom functionality**
   - Follow the existing patterns in `weather-mcp` or `attractions-mcp` folders
   - Implement your custom tools and functionality
   - for any additional guidance you can check here https://github.com/modelcontextprotocol/python-sdk
