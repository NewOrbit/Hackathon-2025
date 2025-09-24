"""
DeepseekTravels API Server

FastAPI backend that replicates the Jupyter notebook functionality
with proper LangChain agent and MCP integration.
"""

import os
import sys
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add the parent directory to the path to import from agent folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'agent'))

from dotenv import load_dotenv

# LangChain imports
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# Official MCP adapter imports for HTTP transport
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'src', 'agent', '.env'))

# Global variables for agent
agent_executor: Optional[AgentExecutor] = None
mcp_client: Optional[MultiServerMCPClient] = None
tools = []

# DeepseekTravels System Prompt (copied from notebook)
DEEPSEEKTRAVELS_SYSTEM_PROMPT = """
You are DeepseekTravels, an intelligent travel packing assistant. Your goal is to generate optimized packing lists that consider:

CORE RESPONSIBILITIES:
• Generate comprehensive packing lists based on destination, weather, activities, and trip length
• Respect capacity constraints (backpack volume, weight limits) and airline restrictions
• Integrate weather forecasts to recommend appropriate clothing and gear
• Check security restrictions and baggage rules for specific airlines/routes
• Suggest relevant bookings (flights, hotels, activities) with explicit confirmation required
• Provide keep-it-simple mode for concise, printable checklists

TOOL USAGE ORDER:
1. Get weather forecast for destination and dates
2. Check travel requirements (visas, documents, security restrictions) 
3. Check airline baggage rules if airline specified
4. Generate packing list considering all factors
5. For bookings: search → present summary → get explicit confirmation → book

CONSTRAINTS HANDLING:
• Always ask for capacity (L), max weight (kg), airline, and activity types if not provided
• Scale clothing quantities based on trip length and laundry access
• Remove/replace items to fit within capacity using priority-based selection
• Replace large liquids with travel sizes for airline compliance
• Flag restricted items and suggest alternatives

BOOKING CONFIRMATION GATES:
• NEVER book without explicit user confirmation
• Present structured summary: item, price, dates, cancellation policy
• Ask "Shall I proceed with this booking?" before calling confirm_booking
• Use hold_booking first, then confirm_booking only after user approval

SCOPE GUARDRAILS:
• Focus ONLY on travel planning and packing
• Refuse non-travel requests politely: "I specialize in travel packing assistance"
• No medical/legal advice beyond linking to official sources
• Emphasize mock data warnings in Phase 1

TOKEN EFFICIENCY:
• Batch parallel tool calls where possible (weather + requirements)
• Use structured, terse outputs in keep-it-simple mode
• Summarize long tool results focusing on actionable information
• Limit tool calls per turn (≤4 unless critical)

OUTPUT FORMAT:
• Use clear categories: Clothing, Electronics, Toiletries, Documents, etc.
• Show quantities, estimated weight/volume, and rationale
• Highlight essential vs. nice-to-have items
• Include capacity analysis: "Uses 18L of your 28L backpack (64%)"
• End with key reminders and any restriction warnings

Remember: You are helpful, thorough, and safety-conscious while respecting user constraints and preferences.
"""

async def create_mcp_tools():
    """Create MCP tools using the official LangChain MCP adapter with HTTP transport"""
    global mcp_client
    
    try:
        # Define MCP server configurations
        server_configs = {
            "weather": {
                "transport": "streamable_http",
                "url": os.getenv("WEATHER_MCP_URL", "http://127.0.0.1:8009/mcp/")
            },
            "attractions": {
                "transport": "streamable_http",
                "url": os.getenv("ATTRACTIONS_MCP_URL", "http://127.0.0.1:8008/mcp/")
            },
            "travel_requirements": {
                "transport": "streamable_http",
                "url": os.getenv("TRAVEL_REQUIREMENTS_MCP_URL", "http://127.0.0.1:8010/mcp/")
            },
            "booking": {
                "transport": "streamable_http",
                "url": os.getenv("BOOKING_MCP_URL", "http://127.0.0.1:8011/mcp/")
            }
        }
        
        print("🔗 Connecting to MCP servers...")
        for name, config in server_configs.items():
            print(f"   • {name}: {config['url']}")
        
        # Create the multi-server MCP client
        mcp_client = MultiServerMCPClient(server_configs)
        
        # Get available tools from all servers
        tools = await mcp_client.get_tools()
        
        print(f"🛠️  Loaded {len(tools)} tools from {len(server_configs)} MCP servers")
        
        return tools
        
    except Exception as e:
        print(f"❌ Error connecting to MCP servers: {e}")
        print("   Make sure all MCP servers are running:")
        for name, config in server_configs.items():
            print(f"   • {name}: uv run main.py (in src/mcp/{name.replace('_', '-')}-mcp/)")
        raise

async def setup_agent():
    """Setup the DeepseekTravels agent with Azure OpenAI and MCP tools"""
    global agent_executor, tools
    
    try:
        # Load MCP tools
        tools = await create_mcp_tools()
        print(f"🧰 Loaded {len(tools)} MCP tools")
        
        # Initialize Azure OpenAI
        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION", "2024-12-01-preview"),
            azure_deployment=os.getenv("DEPLOYMENT_NAME", "gpt-5-nano"),
            temperature=0.1,  # Lower temperature for consistent packing advice
            verbose=True
        )
        
        print(f"🧠 Azure OpenAI initialized: {os.getenv('DEPLOYMENT_NAME', 'gpt-5-nano')}")
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", DEEPSEEKTRAVELS_SYSTEM_PROMPT),
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
        return agent_executor
        
    except Exception as e:
        print(f"❌ Error setting up agent: {e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting DeepseekTravels API Server...")
    try:
        await setup_agent()
        print("✅ Agent initialization complete!")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        # Continue anyway - will show errors to user
    
    yield
    
    # Shutdown
    print("🛑 Shutting down DeepseekTravels API Server...")
    global mcp_client
    if mcp_client:
        try:
            await mcp_client.close()
            print("✅ MCP client connections closed")
        except Exception as e:
            print(f"⚠️ Error closing MCP client: {e}")

# Create FastAPI app
app = FastAPI(
    title="DeepseekTravels API",
    description="Intelligent travel packing assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    agent_ready: bool
    mcp_servers: Dict[str, str]
    tools_count: int

class ServerStatusResponse(BaseModel):
    servers: Dict[str, Dict[str, Any]]

# Session storage (in production, use Redis or database)
sessions: Dict[str, ConversationBufferMemory] = {}

def get_or_create_session(session_id: str) -> ConversationBufferMemory:
    """Get or create a conversation session"""
    if session_id not in sessions:
        sessions[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    return sessions[session_id]

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    global agent_executor, mcp_client, tools
    
    mcp_status = {}
    if mcp_client:
        # Check MCP server status
        server_configs = {
            "weather": "http://127.0.0.1:8009",
            "attractions": "http://127.0.0.1:8008", 
            "travel_requirements": "http://127.0.0.1:8010",
            "booking": "http://127.0.0.1:8011"
        }
        
        for name, url in server_configs.items():
            try:
                # This is a simple check - in practice you'd ping the actual servers
                mcp_status[name] = "connected" if mcp_client else "disconnected"
            except:
                mcp_status[name] = "error"
    else:
        mcp_status = {name: "disconnected" for name in ["weather", "attractions", "travel_requirements", "booking"]}
    
    return HealthResponse(
        status="healthy" if agent_executor else "initializing",
        agent_ready=agent_executor is not None,
        mcp_servers=mcp_status,
        tools_count=len(tools)
    )

@app.get("/servers/status", response_model=ServerStatusResponse)
async def server_status():
    """Get detailed server status"""
    import httpx
    
    servers = {
        "weather": {"url": "http://127.0.0.1:8009", "name": "Weather"},
        "attractions": {"url": "http://127.0.0.1:8008", "name": "Attractions"},
        "travel_requirements": {"url": "http://127.0.0.1:8010", "name": "Travel Requirements"},
        "booking": {"url": "http://127.0.0.1:8011", "name": "Booking"}
    }
    
    status_results = {}
    
    async with httpx.AsyncClient(timeout=3.0) as client:
        for key, info in servers.items():
            try:
                response = await client.get(f"{info['url']}/health")
                if response.status_code == 200:
                    status_results[key] = {
                        "status": "connected",
                        "name": info["name"],
                        "url": info["url"],
                        "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0
                    }
                else:
                    status_results[key] = {
                        "status": "error",
                        "name": info["name"],
                        "url": info["url"],
                        "error": f"HTTP {response.status_code}"
                    }
            except Exception as e:
                status_results[key] = {
                    "status": "disconnected",
                    "name": info["name"],
                    "url": info["url"],
                    "error": str(e)
                }
    
    return ServerStatusResponse(servers=status_results)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Main chat endpoint that processes user messages"""
    global agent_executor
    
    if not agent_executor:
        raise HTTPException(
            status_code=503, 
            detail="Agent not ready. Please check that all MCP servers are running and try again."
        )
    
    try:
        # Get or create session
        session_memory = get_or_create_session(chat_message.session_id)
        
        # Update agent executor with session memory
        agent_executor.memory = session_memory
        
        # Process the message
        response = await agent_executor.ainvoke({"input": chat_message.message})
        
        return ChatResponse(
            response=response["output"],
            session_id=chat_message.session_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        print(f"❌ Error processing chat message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your request: {str(e)}"
        )

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear a conversation session"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    return {"sessions": list(sessions.keys()), "count": len(sessions)}

if __name__ == "__main__":
    print("🚀 Starting DeepseekTravels API Server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )