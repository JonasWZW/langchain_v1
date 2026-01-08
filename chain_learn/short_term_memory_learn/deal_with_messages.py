# -*- coding:utf-8 -*-
"""
启用短期记忆后，长对话可能会超出 LLM 的上下文窗口。常见解决方案有：
trim  before_model middleware
delete after_model middleware
summarize  SummarizationMiddleware
custom
"""


def before():
    from langchain.messages import RemoveMessage
    from langgraph.graph.message import REMOVE_ALL_MESSAGES
    from langgraph.checkpoint.memory import InMemorySaver
    from langchain.agents import create_agent, AgentState
    from langchain.agents.middleware import before_model
    from langchain_core.runnables import RunnableConfig
    from langgraph.runtime import Runtime
    from typing import Any

    @before_model
    def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        """Keep only the last few messages to fit context window."""
        messages = state["messages"]

        if len(messages) <= 3:
            return None  # No changes needed

        first_msg = messages[0]
        recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
        new_messages = [first_msg] + recent_messages

        return {
            "messages": [
                RemoveMessage(id=REMOVE_ALL_MESSAGES),
                *new_messages
            ]
        }

    agent = create_agent(
        "gpt-5-nano",
        tools=[],
        middleware=[trim_messages],
        checkpointer=InMemorySaver()
    )

    config: RunnableConfig = {"configurable": {"thread_id": "1"}}

    agent.invoke({"messages": "hi, my name is bob"}, config)
    agent.invoke({"messages": "write a short poem about cats"}, config)
    agent.invoke({"messages": "now do the same but for dogs"}, config)
    final_response = agent.invoke({"messages": "what's my name?"}, config)

    final_response["messages"][-1].pretty_print()
    """
    ================================== Ai Message ==================================

    Your name is Bob. You told me that earlier.
    If you'd like me to call you a nickname or use a different name, just say the word.
    """


def after():
    from langchain.messages import RemoveMessage
    from langgraph.checkpoint.memory import InMemorySaver
    from langchain.agents import create_agent, AgentState
    from langchain.agents.middleware import after_model
    from langgraph.runtime import Runtime

    @after_model
    def validate_response(state: AgentState, runtime: Runtime) -> dict | None:
        """Remove messages containing sensitive words."""
        STOP_WORDS = ["password", "secret"]
        last_message = state["messages"][-1]
        if any(word in last_message.content for word in STOP_WORDS):
            return {"messages": [RemoveMessage(id=last_message.id)]}
        return None

    agent = create_agent(
        model="gpt-5-nano",
        tools=[],
        middleware=[validate_response],
        checkpointer=InMemorySaver(),
    )
