# -*- coding:utf-8 -*-
"""
runtime: ToolRuntime 具备几乎全部所需

    state: StateT
    context: ContextT
    config: RunnableConfig
    stream_writer: StreamWriter
    tool_call_id: str | None
    store: BaseStore | None
"""
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.types import Command


# 访问state 与 修改state

# Access the current conversation state
@tool
def summarize_conversation(
        runtime: ToolRuntime
) -> str:
    """Summarize the conversation so far."""
    messages = runtime.state["messages"]

    human_msgs = sum(1 for m in messages if m.__class__.__name__ == "HumanMessage")
    ai_msgs = sum(1 for m in messages if m.__class__.__name__ == "AIMessage")
    tool_msgs = sum(1 for m in messages if m.__class__.__name__ == "ToolMessage")

    return f"Conversation has {human_msgs} user messages, {ai_msgs} AI responses, and {tool_msgs} tool results"


# Access custom state fields
@tool
def get_user_preference(
        pref_name: str,
        runtime: ToolRuntime  # ToolRuntime parameter is not visible to the model
) -> str:
    """Get a user preference value."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")


# Update the conversation history by removing all messages
@tool
def clear_conversation() -> Command:
    """Clear the conversation history."""

    return Command(
        update={
            "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)],
        }
    )


# Update the user_name in the agent state
@tool
def update_user_name(
        new_name: str,
        runtime: ToolRuntime
) -> Command:
    """Update the user's name."""
    return Command(update={"user_name": new_name})
