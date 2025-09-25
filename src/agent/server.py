# Step to ensure that the venv is being used for the project not local copies, should point at .venv in project.
import sys, shutil

from fastapi import FastAPI
from pydantic import BaseModel
print("python:", sys.executable)
print("uv:", shutil.which("uv")) 

# LangChain + MCP Setup for Attractions Booking (HTTP-based for Jupyter)
import os
from dotenv import load_dotenv
import asyncio
import json
import requests
from typing import Dict, Any, List
from contextlib import asynccontextmanager


# LangChain imports
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# Official MCP adapter imports for HTTP transport
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from fastapi.middleware.cors import CORSMiddleware

from attractions import main, ask_assistant

# Load environment variables
load_dotenv()

print("✅ Updated imports with official MCP adapter loaded successfully!")

# MCP Client Setup using Official Adapter with HTTP Transport
import subprocess
import time
from fastapi.responses import FileResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await main()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    message: str

@app.post("/")
async def send_message(item: Item):
    return await ask_assistant(item.message)

@app.get("/")
async def root():
    return FileResponse("chat.html")