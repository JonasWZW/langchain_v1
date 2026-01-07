# -*- coding:utf-8 -*-

"""
Tool calling(也就是function calling)  工具调用
模型可以请求调用执行任务的工具，例如从数据库获取数据、搜索网络或运行代码。工具是一对：
1.A schema, including the name of the tool, a description, and/or argument definitions (often a JSON schema)
一个模式，包括工具的名称、描述和/或参数定义（通常是 JSON 模式）
2。A function or   一个函数或coroutine  协程 to execute.  来执行。


"""
from config import deepseek
from langchain.tools import tool

model = deepseek


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


# model必须使用bind_tools绑定工具集合，这样model才会调用。
# （个人觉得应该就是本质使用了模型的能力，或者简单的来说就是提示词功能+训练的可以调用工具的模型整合了这方面能力）
model_with_tools = model.bind_tools([get_weather])

"""
在使用自定义工具时，模型的响应会包含一个执行工具的请求。
当单独使用模型时，需要你自行执行请求的工具并将结果返回给模型，以便在后续推理中使用。
当使用代理时，代理循环将为你处理工具执行循环。
"""
# 只使用model的时候，需要自己收集聊天记录
chat_history = [
    ("human", "What's the weather like in Boston?")
]
response = model_with_tools.invoke(chat_history)
# 此时response是AIMessage，他想调用tool。
print(response)
chat_history.append(response)
for tool_call in response.tool_calls:
    # View tool calls made by the model
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
    msg = get_weather.invoke(tool_call)
    print(msg)
    chat_history.append(msg)

# 最后需要手动处理结果，然后加入进去
resp = model_with_tools.invoke(chat_history)
print(resp)
