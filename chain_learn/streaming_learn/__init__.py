# -*- coding:utf-8 -*-
"""

StreamMode = Literal[
    "values", "updates", "checkpoints", "tasks", "debug", "messages", "custom"
]
How the stream method should emit outputs.

- `"values"`: Emit all values in the state after each step, including interrupts.
    When used with functional API, values are emitted once at the end of the workflow.
- `"updates"`: Emit only the node or task names and updates returned by the nodes or tasks after each step.
    If multiple updates are made in the same step (e.g. multiple nodes are run) then those updates are emitted separately.
- `"custom"`: Emit custom data using from inside nodes or tasks using `StreamWriter`.
- `"messages"`: Emit LLM messages token-by-token together with metadata for any LLM invocations inside nodes or tasks.
- `"checkpoints"`: Emit an event when a checkpoint is created, in the same format as returned by `get_state()`.
- `"tasks"`: Emit events when tasks start and finish, including their results and errors.
- `"debug"`: Emit `"checkpoints"` and `"tasks"` events for debugging purposes.

StreamMode有很多种，配合stream()使用，不同的StreamMode返回的结果是不同的。
常见的有四种
1 values(全量状态模式)
    含义：
        每次图中的一个节点（Node）执行完毕后，LangGraph 会输出当前图的完整状态（Full State）。
    特点：
        累积性：你会看到状态是如何一步步变“大”或变化的。
        用途：适用于调试，或者前端需要每次都重新渲染整个上下文的场景。
2 updates(增量更新模式)
    含义：
        每次节点执行完毕后，只输出该节点返回的更新内容（Delta），而不是整个状态。
    特点：
        原子性：你清楚地知道是由哪个节点产生了哪个输出。
        用途：构建复杂的流式 UI，只需将新产生的数据追加到现有视图中，无需刷新整个状态。
3 custom(自定义数据模式)
    含义：
        允许你在节点内部使用 StreamWriter 手动发送数据。这些数据不一定要是状态的一部分。
    特点：
        灵活性：可以发送进度条信息、中间思考过程（CoT）、调试日志等，而不会污染主程序的 State。
        用途：例如在一个耗时节点中，每处理 10% 就像前端发送一个进度信号。
4 messages (LLM 消息流模式)
    含义：
        这是专门为 LLM（大语言模型）设计的。如果你的节点内部调用了支持流式输出的 ChatModel（如 ChatOpenAI），该模式会拦截并输出 LLM 生成的每一个 Token。
    特点：
        细粒度：Token-by-token 的输出，用于实现类似 ChatGPT 的打字机效果。
        元数据：除了文本块，还包含发送者信息、ID 等。
"""