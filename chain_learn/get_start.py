from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver

"""
overview是一个简单的玩具代理，不能作用于生产。

Build a real-world agent  
构建现实世界的智能体

Detailed system prompts for better agent behavior
详细的系统提示以改善智能体行为
Create tools that integrate with external data
创建与外部数据集成的工具
Model configuration for consistent responses
模型配置以获得一致响应
Structured output for predictable results
结构化输出以获得可预测结果
Conversational memory for chat-like interactions
对话记忆以实现类似聊天的交互
Create and run the agent create a fully functional agent
创建并运行代理，创建一个完全功能性的代理
"""

# 1 Define the system prompt  定义系统提示
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""


# 2 Create tools  创建工具
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@dataclass
class UserContext:
    """Custom runtime context schema."""
    # 定义上下文和相关属性
    user_id: str


@tool
def get_user_location(runtime: ToolRuntime[UserContext]) -> str:
    """Retrieve user information based on user ID."""
    # 使用ToolRuntime可以注入运行时上下文
    # ToolRuntime[UserContext] 代表，本agent的创建的时候的context是UserContext
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


# 3 Configure your model  配置你的模型
from config import deepseek


# 4 Define response format  定义响应格式
# We use a dataclass here, but Pydantic models are also supported.
# 我感觉使用pydantic比较好，可以进行类型检测和限制，例如你有些是枚举的，有些有格式要求。
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


# 5 Add memory  添加记忆
# 这个就是短期记忆，说白了就是，能够把State的messages给记忆下来，每次都可以把相同的thread_id的历史聊天记录发过去并且管理好

checkpointer = InMemorySaver()

agent = create_agent(
    model=deepseek,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=UserContext,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config=config,
    context=UserContext(user_id="1")
)

print(response['structured_response'])

# Note that we can continue the conversation using the same `thread_id`.
response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config=config,
    context=UserContext(user_id="1")
)

print(response['structured_response'])
