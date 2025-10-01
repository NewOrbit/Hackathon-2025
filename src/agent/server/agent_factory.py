from __future__ import annotations

from typing import Dict, List

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import SystemMessage
from mcp_loader import load_mcp_tools_sync


def _build_prompt(system_prompt: str, tool_descriptions: List[str]) -> ChatPromptTemplate:
    tool_section = "\n".join(f"- {line}" for line in tool_descriptions if line)
    instructions = system_prompt
    if tool_section:
        instructions += "\n\nYou can call the following tools when needed:\n" + tool_section
    aim = (
        "Use tools to fetch macro estimates, or nutrition plans "
        "whenever it helps answer the user."
    )
    instructions += f"\n\n{aim}"
    return ChatPromptTemplate.from_messages(
        [
            ("system", instructions),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )


def create_agent_runner(llm, system_prompt: str):
    tools, tool_descriptions = load_mcp_tools_sync()
    prompt = _build_prompt(system_prompt, tool_descriptions)
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    history_store: Dict[str, ChatMessageHistory] = {}

    def get_history(config: Dict):
        if isinstance(config, str):
            session_id = config
        else:
            session_id = config.get("configurable", {}).get("session_id", "default")
        history = history_store.get(session_id)
        if history is None:
            history = ChatMessageHistory()
            history.add_message(SystemMessage(content=prompt.messages[0].prompt.template))
            history_store[session_id] = history
        return history

    runnable = RunnableWithMessageHistory(
        executor,
        get_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return runnable


