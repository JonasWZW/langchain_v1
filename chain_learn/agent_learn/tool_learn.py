# -*- coding:utf-8 -*-
"""
Tools give agents the ability to take actions. Agents go beyond simple model-only tool binding by facilitating:
工具赋予代理执行操作的能力。代理通过促进以下方面，超越了简单的模型仅工具绑定：
Multiple tool calls in sequence (triggered by a single prompt)
连续的多个工具调用（由单个提示触发）
Parallel tool calls when appropriate
在适当的时候并行调用工具
Dynamic tool selection based on previous results
基于先前结果动态选择工具
Tool retry logic and error handling
工具重试逻辑和错误处理
State persistence across tool calls
跨工具调用的状态持久化

langchain的agent，不仅仅是绑定了工具这么简单，感觉他是实现了react的基础上，又加入了一些plan等相关
"""
import traceback
from typing import Callable

from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command

from config import deepseek
from langchain.tools import tool
from langchain.agents import create_agent

"""
# 1 Defining tools  定义工具

Tools can be specified as plain Python functions or
工具可以指定为普通的 Python 函数或coroutines  协程.
The tool decorator can be used to customize tool names, descriptions, argument schemas, and other properties.
工具装饰器可用于自定义工具名称、描述、参数模式和其他属性。
"""


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"


tools = [search, get_weather]

agent = create_agent(deepseek, tools=tools)
"""
# 2 Tool error handling  工具错误处理
就类似于一些web框架的最佳实践一样，可以定义一个全局的wrap_tool_call中间件，
让他来统一处理调用工具的时候，tool_call发生的异常，并且将异常信息返回给llm，指导llm重新调用
并且如果发生某个tool的多次调用失败，应该强制触发终止

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
"""


@wrap_tool_call
def handler_tool_call_exception(request: ToolCallRequest,
                                handler: Callable[[ToolCallRequest], ToolMessage | Command], ) -> ToolMessage | Command:
    """Handle tool execution errors with custom messages."""
    try:
        # tool_call_error_time = request.runtime.state.get("tool_call_error_time", 0 )
        # if tool_call_error_time > 3:
        #     return Command(goto="__END__")
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        print(traceback.format_exc())
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )


agent_with_tool_except_handler = create_agent(
    model=deepseek,
    tools=tools,
    middleware=[handler_tool_call_exception]
)
