"""
DeepseekTravels API Server - Simplified Version

FastAPI backend that provides a simple chat interface while 
MCP servers are being set up. This can be extended later 
with full LangChain integration.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from dotenv import load_dotenv

# LangChain imports
from langchain.agents import AgentExecutor

# Official MCP adapter imports for HTTP transport

from contextlib import asynccontextmanager

from agent import setup_agent

origins = [
    "http://localhost",
    "http://localhost:5173",
]

load_dotenv('.env')

agent_executor: Optional[AgentExecutor] = None
tools: Optional[list] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("🚀 Starting DeepseekTravels Agent...")
    global agent_executor, tools

    agent_executor, tools = await setup_agent(system_prompt=DEEPSEEKTRAVELS_SYSTEM_PROMPT)

    print("✅ DeepseekTravels Agent is ready!")
    yield

# Create FastAPI app
app = FastAPI(
    title="DeepseekTravels API",
    description="Intelligent travel packing assistant API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

DEEPSEEKTRAVELS_SYSTEM_PROMPT = """
You are DeepseekTravels, an intelligent travel packing assistant. Your goal is to generate optimized packing lists.
"""

async def generate_response(message: str) -> str:
    """Process user input and return LLM response using MCP tools"""
    global agent_executor

    if not agent_executor:
        return "Agent not initialized. Please run the initialization cell first."
    
    try:
        # Use the agent to process the input and get intermediate steps
        result = await agent_executor.ainvoke({"input": message})
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

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """Main chat endpoint that processes user messages"""
    try:
        # Generate response (simplified version)
        print(f"Received message: {req.message}")
        response_text = await generate_response(req.message)
        print(f"Response: {response_text}")
        
        return {"response": response_text}        
    except Exception as e:
        print(f"Error processing chat message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your request: {str(e)}"
        )

if __name__ == "__main__":
    print("🚀 Starting DeepseekTravels API Server (Simplified Mode)...")
    print("   This version provides LangChain integration with MCP servers.")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )