from __future__ import annotations

import os
import uuid
from typing import Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# LangChain / OpenAI
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.tools import ToolException

from agent_factory import create_agent_runner

load_dotenv()

app = FastAPI(title="Agent Server", version="0.1.0")

# Allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InitResponse(BaseModel):
    sessionId: str


class ChatRequest(BaseModel):
    sessionId: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    sessionId: str
    output: str


def _get_llm():
    # Prefer Azure if configured
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("DEPLOYMENT_NAME"):
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION", "2024-12-01-preview"),
            deployment_name=os.getenv("DEPLOYMENT_NAME"),
            temperature=1,
        )
    # Fallback to OpenAI
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


SYSTEM_PROMPT = (
    "You are an assistant helping with travel, weather, macros, and nutrition planning. "
    "Ask clarifying questions when needed and provide concise, actionable answers."
)


AGENT_RUNNER = create_agent_runner(_get_llm(), SYSTEM_PROMPT)


def _ensure_session_id(session_id: Optional[str]) -> str:
    return session_id or str(uuid.uuid4())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/init", response_model=InitResponse)
def init_session():
    sid = _ensure_session_id(None)
    return InitResponse(sessionId=sid)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = _ensure_session_id(req.sessionId)
    try:
        response = await AGENT_RUNNER.ainvoke(
            {"input": req.message},
            config={"configurable": {"session_id": session_id}},
        )
        output = response.get("output") if isinstance(response, dict) else str(response)
        return ChatResponse(sessionId=session_id, output=output)
    except ToolException as tool_err:
        message = (
            "Sorry, one of the MCP tools failed: "
            f"{tool_err}. Please supply the required details or try again."
        )
        return ChatResponse(sessionId=session_id, output=message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)


