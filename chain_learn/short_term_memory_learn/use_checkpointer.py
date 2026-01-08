# -*- coding:utf-8 -*-

from langchain.agents import create_agent, AgentState
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolRuntime

from config import deepseek

"""
Usage  使用
要向代理添加短期记忆（线程级持久性），您需要在创建代理时指定 checkpointer 。

LangChain 的代理将短期记忆(checkpointer)作为代理状态(state的messages)的一部分进行管理。
通过将这些信息存储在图的状态（state）中，代理可以在不同线程之间保持分离的同时，访问给定对话的完整上下文。
状态通过检查点器持久化到数据库（或内存）中，以便线程可以在任何时候被恢复。
短期记忆在代理被调用或一个步骤（如工具调用）完成时更新，并在每个步骤开始时读取状态。
（即每产生一个新的消息，就会把他通过策略处理到state的message中，后续的调用，会将前面的message全部传入）

"""


@tool
def get_user_info() -> str:
    """Look up user info."""
    return "Bob, 18 years old, male, work in bank, hobbies: reading and swimming"


# 默认的state是langchain.agents.middleware.types.AgentState
"""
class AgentState(TypedDict, Generic[ResponseT]):
    messages: Required[Annotated[list[AnyMessage], add_messages]]
    jump_to: NotRequired[Annotated[JumpTo | None, EphemeralValue, PrivateStateAttr]]
    structured_response: NotRequired[Annotated[ResponseT, OmitFromInput]]
"""
agent = create_agent(
    deepseek,
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

# 短期记忆checkpoint必须配合langchain_core.runnables.config.RunnableConfig的configurable的thread_id进行使用。
agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    {"configurable": {"thread_id": "1"}},
)


# 相同的thread_id，会从checkpointer中读取短期记忆，并入messages里面，从而进行调用


class CustomAgentState(AgentState):
    user_id: str
    preferences: dict


agent_with_customState = create_agent(
    deepseek,
    tools=[get_user_info],
    state_schema=CustomAgentState,
    checkpointer=InMemorySaver(),
)

# Custom state can be passed in invoke
result = agent_with_customState.invoke(
    {
        "messages": [{"role": "user", "content": "Hello"}],
        "user_id": "user_123",
        "preferences": {"theme": "dark"}
    },
    {
        "configurable":
            {
                "thread_id": "1"
            }
     }
)
