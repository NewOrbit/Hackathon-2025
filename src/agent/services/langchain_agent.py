"""LangChain agent builder for DeepseekTravels."""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, Tuple, Callable

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import ToolException, StructuredTool

from langchain_mcp_adapters.client import MultiServerMCPClient
from .safety_tools import create_safety_tool
MANDATORY_TOOL_ARGS: Dict[str, tuple[str, ...]] = {
    "get_current_weather": ("location",),
    "get_weather_forecast": ("location",),
    "get_attraction_details": ("attraction_id",),
    "book_attraction": ("attraction_id", "visitor_name", "email", "visit_date"),
    "search_flights": ("origin", "destination", "depart_date"),
    "search_hotels": ("destination", "check_in", "check_out"),
    "search_activities": ("destination", "start_date"),
    "get_visa_requirements": ("nationality", "destination_country"),
    "check_baggage_allowance": ("airline",),
    "hold_booking": ("booking_type", "booking_payload"),
    "confirm_booking": ("hold_id",),
}


def _guard_tool(tool: Any) -> Any:
    required = MANDATORY_TOOL_ARGS.get(tool.name)
    if not required:
        return tool

    args_schema = getattr(tool, "args_schema", None)

    def _validate(params: Dict[str, Any]):
        missing = [arg for arg in required if not params.get(arg)]
        if missing:
            raise ToolException(
                "Missing required parameters: "
                + ", ".join(missing)
                + ". Please gather these trip details before calling this tool."
            )

    if hasattr(tool, "ainvoke"):
        async def async_wrapper(**kwargs):
            _validate(kwargs)
            return await tool.ainvoke(kwargs)
    else:
        async_wrapper = None

    def sync_wrapper(**kwargs):
        _validate(kwargs)
        if hasattr(tool, "invoke"):
            return tool.invoke(kwargs)
        return _run_async(tool.ainvoke(kwargs))

    return StructuredTool(
        name=tool.name,
        description=tool.description,
        args_schema=args_schema,
        func=sync_wrapper,
        coroutine=async_wrapper,
    )

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "comprehensive_system_prompt.txt")
with open(PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
    SYSTEM_PROMPT = prompt_file.read()


def _run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:  # pragma: no cover - defensive branch
        return loop.run_until_complete(coro)


def build_langchain_agent() -> Tuple[AgentExecutor, MultiServerMCPClient]:
    required_env = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_DEPLOYMENT",
    ]
    missing = [key for key in required_env if not os.getenv(key)]
    if missing:
        raise RuntimeError(f"Missing required Azure OpenAI env vars: {', '.join(missing)}")

    mcp_config: dict[str, dict[str, str]] = {
        "attractions": {
            "transport": "streamable_http",
            "url": os.getenv("ATTRACTIONS_MCP_URL", "http://localhost:8008"),
        },
        "weather": {
            "transport": "streamable_http",
            "url": os.getenv("WEATHER_MCP_URL", "http://localhost:8009"),
        },
        "requirements": {
            "transport": "streamable_http",
            "url": os.getenv("REQUIREMENTS_MCP_URL", "http://localhost:8010"),
        },
        "booking": {
            "transport": "streamable_http",
            "url": os.getenv("BOOKING_MCP_URL", "http://localhost:8011"),
        },
    }

    mcp_client = MultiServerMCPClient(mcp_config)
    tools = asyncio.run(mcp_client.get_tools())

    temperature_env = os.getenv("AZURE_OPENAI_TEMPERATURE")
    temperature = float(temperature_env) if temperature_env else 1.0

    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=temperature,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    guarded_tools = [_guard_tool(tool) for tool in tools]

    agent = create_tool_calling_agent(llm, guarded_tools, prompt)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    executor = AgentExecutor(
        agent=agent,
        tools=guarded_tools,
        memory=memory,
        verbose=False,
        handle_parsing_errors=True,
    )
    return executor, mcp_client
