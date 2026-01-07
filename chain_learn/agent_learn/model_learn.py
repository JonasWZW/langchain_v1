# -*- coding:utf-8 -*-
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call

# 1 Static model  静态模型
# 静态模型在创建代理时配置一次，并在整个执行过程中保持不变。这是最常见和最直接的方法。
# deepseek这个就是

# 2 Dynamic model  动态模型
# 动态模型是在运行时，基于当前状态以及上下文。这使得能够实现复杂的路由逻辑和成本优化。
# 要使用动态模型，请使用 @wrap_model_call 装饰器创建中间件，该中间件会修改请求中的模型：

from config import deepseek, deepseek_r1

basic_model = deepseek
advanced_model = deepseek_r1


# 复杂的中间件，继承AgentMiddleware
# 简单的使用对应的几个装饰器
@wrap_model_call
def dynamic_choose_model_by_msg_count(request: ModelRequest,
                                      handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advanced_model
    else:
        model = basic_model
    # 异常这里需要处理？
    return handler(request.override(model=model))


tools = []

agent = create_agent(
    model=basic_model,
    # tools=tools,
    middleware=[dynamic_choose_model_by_msg_count]
)
