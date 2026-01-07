# -*- coding:utf-8 -*-

"""
Q: langchain和langgraph，如何选择？
如果你想要快速构建代理和自主应用程序，我们推荐使用 LangChain。
当你有更高级的需求，需要结合确定性流程和代理式流程、大量定制以及严格控制延迟时，
请使用我们的低级代理编排框架和运行时 LangGraph。

Q: langchain的功能
LangChain agents 是基于 LangGraph 构建的，以提供持久执行、流式处理、人机交互、持久化等功能。
"""

from langchain.agents import create_agent

from config import deepseek


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_agent(
    model=deepseek,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
resp = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
