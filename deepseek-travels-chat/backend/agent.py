import os

from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from langchain_mcp_adapters.client import MultiServerMCPClient

server_configs = {
    "weather": {
        "transport": "streamable_http",
        "url": os.getenv("WEATHER_MCP_URL", "http://127.0.0.1:8009/mcp/")
    },
    "attractions": {
        "transport": "streamable_http",
        "url": os.getenv("ATTRACTIONS_MCP_URL", "http://127.0.0.1:8008/mcp/")
    },
    "requirements": {
        "transport": "streamable_http",
        "url": os.getenv("REQUIREMENTS_MCP_URL", "http://127.0.0.1:8010/mcp/")
    },
    "booking": {
        "transport": "streamable_http",
        "url": os.getenv("BOOKING_MCP_URL", "http://127.0.0.1:8011/mcp/")
    }
}

def create_mcp_client():
    """Create MCP tools using the official LangChain MCP adapter with HTTP transport"""
    try:
        # Define MCP server configurations
        print("🔗 Connecting to MCP servers...")
        for name, config in server_configs.items():
            print(f"   • {name}: {config['url']}")
        
        # Create the multi-server MCP client
        mcp_client = MultiServerMCPClient(server_configs)
        
        return mcp_client
        
    except Exception as e:
        print(f"❌ Error connecting to MCP servers: {e}")
        print("   Make sure all MCP servers are running:")
        for name, config in server_configs.items():
            print(f"   • {name}: uv run main.py (in src/mcp/{name.replace('_', '-')}-mcp/)")
        raise

async def setup_agent(system_prompt: str):
    """Setup the DeepseekTravels agent with Azure OpenAI and MCP tools"""
    global agent_executor, tools
    
    try:
        # Load MCP tools
        mcp_client = create_mcp_client()
        print("MCP client created, loading tools...")
        tools = await mcp_client.get_tools()
        print(f"🧰 Loaded {len(tools)} MCP tools")
        
        # Initialize Azure OpenAI
        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION", "2024-12-01-preview"),
            azure_deployment=os.getenv("DEPLOYMENT_NAME", "gpt-5-nano"),
            temperature=1,  # Lower temperature for consistent packing advice
            verbose=True
        )
        
        print(f"🧠 Azure OpenAI initialized: {os.getenv('DEPLOYMENT_NAME', 'gpt-5-nano')}")
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        
        # Create agent
        agent = create_tool_calling_agent(llm, tools, prompt)
        
        # Create memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        print(f"🤖 DeepseekTravels agent initialized successfully!")
        return [agent_executor, tools]
        
    except Exception as e:
        print(f"❌ Error setting up agent: {e}")
        raise