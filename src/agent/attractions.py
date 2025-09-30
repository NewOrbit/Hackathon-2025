# Step to ensure that the venv is being used for the project not local copies, should point at .venv in project.
import sys, shutil
print("python:", sys.executable)
print("uv:", shutil.which("uv"))

# LangChain + MCP Setup for Attractions Booking (HTTP-based for Jupyter)
import os
from dotenv import load_dotenv
import asyncio
import json
import requests
from typing import Dict, Any, List

# LangChain imports
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# Official MCP adapter imports for HTTP transport
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

# Load environment variables
load_dotenv()

print("✅ Updated imports with official MCP adapter loaded successfully!")

# MCP Client Setup using Official Adapter with HTTP Transport
import subprocess
import time

# Global MCP client for HTTP
mcp_client = None

async def create_mcp_tools():
    """Create MCP tools using the official LangChain MCP adapter with HTTP transport"""
    global mcp_client

    try:
        # Create MultiServerMCPClient with streamable_http transport
        mcp_client = MultiServerMCPClient({
            "attractions": {
                "transport": "streamable_http",
                "url": os.getenv("ATTRACTIONS_MCP_URL")
            },
            "weather": {
                "transport": "streamable_http",
                "url": os.getenv("WEATHER_MCP_URL")
            },
            "packing_list": {
                "transport": "streamable_http",
                "url": os.getenv("PACKING_LIST_MCP_URL")
            },
            "endorsements": {
                "transport": "streamable_http",
                "url": os.getenv("ENDORSEMENTS_MCP_URL")
            },
            "persist": {
                "transport": "streamable_http",
                "url": os.getenv("PERSIST_PACKING_LIST_MCP_URL")
            }
        })

        # Get tools from the MCP server
        tools = await mcp_client.get_tools()
        print(f"Loaded {len(tools)} MCP tools: {[tool.name for tool in tools]}")
        return tools

    except Exception as e:
        print(f"Error connecting to MCP HTTP server: {e}")
        return []

print("🔗 MCP HTTP adapter setup ready!")

# Load MCP Tools using Official Adapter
# The tools will be loaded dynamically when setting up the agent
# No need to manually create tool wrappers - the adapter handles this automatically
print("🛠️ Ready to load MCP tools via official adapter!")

async def setup_agent():
    """Setup LangChain agent with MCP tools using official adapter"""

    # Initialize LLM for Azure OpenAI
    # can get this from Azure Open Ai service -> Azure Ai Foundary Portal
    from langchain_openai import AzureChatOpenAI

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("DEPLOYMENT_NAME"),  # Your Azure deployment name
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_API_VERSION"),
        temperature=1
    )

    # Load MCP tools using official adapter
    tools = await create_mcp_tools()

    if not tools:
        print("No MCP tools loaded. Make sure the MCP server is accessible.")
        return None

    print(f"Loaded {len(tools)} MCP tools: {[tool.name for tool in tools]}")

    # Create system prompt
    system_prompt = """You are a helpful travel assistant that can help users find and book attractions including weather.

    You have access to multiple MCP tools for tourist attractions, including:
    - Searching for attractions by location and category
    - Getting detailed attraction information
    - Booking attractions for visitors
    - Getting random attraction suggestions
    - And more...

    When users ask about travel plans, use these tools to provide comprehensive information.
    Always be helpful and provide practical advice.

    You are also able to generate packing lists based on a given activity. When asked to create a packing list, you
    should also ask the user about the location of their trip, and then check the weather there in order to generate
    a better-tailored list.

    You are also able to accept endorsements from users for this service. You should prompt users
    to give endorsements after you have spoken to them. You should give the users the list of endorsers if you ask for it.
    """

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create agent executor with tool logging callback and verbose output
    agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

    return agent_executor

# Initialize the agent (now async)
agent_executor = None
print("🤖 Agent setup function ready! Run the next cell to initialize.")

# Initialize the agent with MCP tools
async def initialize_agent():
    """Initialize the agent with MCP tools"""
    global agent_executor
    print("Initializing agent with MCP tools...")
    agent_executor = await setup_agent()
    if agent_executor:
        print("LangChain agent with MCP tools ready!")
    else:
        print("Failed to initialize agent. Check MCP server connection.")

# User Input Handler + logged agent steps
async def process_user_input(user_input: str) -> str:
    """Process user input and return LLM response using MCP tools"""
    if not agent_executor:
        return "Agent not initialized. Please run the initialization cell first."

    try:
        # Use the agent to process the input and get intermediate steps
        result = await agent_executor.ainvoke({"input": user_input})
        output = result.get("output") or result.get("final_output") or ""

        # Print intermediate steps if present
        steps = result.get("intermediate_steps") or []
        for step in steps:
            action = None
            observation = None
            if isinstance(step, tuple) and len(step) == 2:
                action, observation = step
            elif isinstance(step, dict) and "action" in step:
                action = step.get("action")
                observation = step.get("observation")
            else:
                continue

            tool_name = getattr(action, "tool", getattr(action, "tool_name", "unknown"))
            tool_args = getattr(action, "tool_input", getattr(action, "input", None))
            print(f"\n--- Tool: {tool_name}")
            print(f"args: {tool_args}")
            if observation is not None:
                print(f"result: {observation}")
            print("---\n")

        return output
    except Exception as e:
        return f"Error processing request: {str(e)}"

# Interactive function for easy testing
async def ask_assistant(question: str):
    """Easy-to-use function for asking the travel assistant"""
    print(f"🧳 User: {question}")
    print("🤖 Assistant:")

    response = await process_user_input(question)
    print(response)
    return response

print("💬 User input handler ready!")

# Test MCP server connectivity and tools
async def test_mcp_connection():
    """Test MCP server connection and list available tools"""
    tools = await create_mcp_tools()
    if tools:
        print(f"MCP HTTP server connected successfully!")
        print(f"Available tools: {[tool.name for tool in tools]}")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
    else:
        print("Failed to connect to MCP HTTP server")

# Test MCP HTTP connection

async def chat_loop():
    print("Type 'exit' to quit. Press Enter on an empty line to skip.")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        await ask_assistant(question)

async def main():
    # Run the initialization
    await initialize_agent()
    await test_mcp_connection()
    # 🚀 EXAMPLE USAGE - Run this cell after setting up your API key!

    # Interactive chat loop — keep asking questions until you exit

# try -
# give me a random attraction
# what about attractions in paris
# more details on eiffel tower
# book eiffel tower

if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(chat_loop())