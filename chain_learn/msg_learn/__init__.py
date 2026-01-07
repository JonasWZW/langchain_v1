# -*- coding:utf-8 -*-
from langchain_core.messages import HumanMessage

"""
content_blocks会自动补充content属性
content_blocks: list[types.ContentBlock] | None = None,
ContentBlock = (
    TextContentBlock
    | InvalidToolCall
    | ReasoningContentBlock
    | NonStandardContentBlock
    | DataContentBlock
    | ToolContentBlock
)
"""

human_message = HumanMessage(content_blocks=[
    {"type": "text", "text": "Hello, how are you?"},
    {"type": "image", "url": "https://example.com/image.jpg"},
])

print(human_message)

"""
消息是进行聊天的基本单元，任何llm都需要维护消息。
上下文工程，说白了就是如何处理好 各种消息，是的本次的llm的输出可以达到最佳的效果。

在langchain中，消息被分类4类
SystemMessage
HumanMessage
AIMessage
ToolMessage

当然还有stream流式调用的时候，对应的XXXChunk，例如AIMessageChunk.......
其中SystemMessage和HumanMessage，差不多平平无奇。
AIMessage和ToolMessage相较于上面的，有很多内容。
AIMessage可以调用多个tool，他有个 tool_calls: list[ToolCall]
ToolMessage则和ToolCall相对应，返回调用的某个tool的信息。
@tool装饰和BaseTool的，都可以invoke(tool_call实例)

langchain v1.0.0
content只能处理字符串，无法解决多模态问题，或者是 文本+图片等问题，不好弄出界限
加入了content_blocks来解决后面的多模态问题

LangChain 提供了一种跨提供商的标准消息内容表示方式。
消息对象实现了一个 content_blocks 属性，该属性将惰性解析 content 属性为标准、类型安全的表示形式。
多模态是指处理不同形式数据的能力，例如文本、音频、图像和视频。LangChain 包括这些数据的标准类型，这些类型可以在不同提供者之间使用。

"""
