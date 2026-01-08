# -*- coding:utf-8 -*-
"""
工具扩展了代理的功能——允许它们获取实时数据、执行代码、查询外部数据库以及在世界中采取行动。

在底层，工具是具有[明确定义的输入和输出的可调用函数]，这些函数会被传递给聊天模型。模型根据对话上下文决定何时调用工具，以及提供什么输入参数。


Accessing Context  访问上下文
为何这很重要：工具在能够访问代理状态、运行时上下文和长期记忆时最为强大。这使得工具能够做出上下文感知的决策、个性化响应，并在对话中保持信息。

运行时上下文提供了一种在运行时将依赖项（如数据库连接、用户 ID 或配置）注入到你的工具中的方法，使它们更易于测试和重用。

工具可以通过 ToolRuntime 参数访问运行时信息，该参数提供
    State - Mutable data that flows through execution (e.g., messages, counters, custom fields)
    状态 - 在执行过程中流动的可变数据（例如，消息、计数器、自定义字段）

    Context - Immutable configuration like user IDs, session details, or application-specific configuration
    上下文 - 不可变的配置，如用户 ID、会话详细信息或特定于应用程序的配置

    Store - Persistent long-term memory across conversations
    存储 - 跨对话的持久长期记忆

    Stream Writer - Stream custom updates as tools execute
    流写入器 - 工具执行时流式传输自定义更新

    Config - RunnableConfig for the execution
    配置 - RunnableConfig 用于执行

    Tool Call ID - ID of the current tool call
    工具调用 ID - 当前工具调用的 ID

ToolRuntime : 一个统一参数，为工具提供对状态、上下文、存储、流式传输、配置和工具调用 ID 的访问。
这取代了使用单独的 InjectedState 、 InjectedStore 、 get_runtime 和 InjectedToolCallId 注释的旧模式。
runtime: ToolRuntime 它会被自动注入，而不会被暴露给 LLM, 对模型是隐藏的。
"""