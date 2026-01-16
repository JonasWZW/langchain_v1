# -*- coding:utf-8 -*-
"""
持久化机制是langgraph的灵魂，它使得langgraph具有了一系列特征
    LangGraph 的“图”逻辑（Pregel）虽然精妙，但真正让它在生产环境中具备“Agent 编排能力”的核心竞争力，就在于这个 Checkpointer 的设计。
    它把复杂的 Agent 状态管理难题，通过一个标准化的接口（BaseCheckpointSaver）给彻底解决了。

    LangGraph 具有内置的持久化层，通过检查点器实现。当你使用检查点器编译图时，检查点器会在每个超级步骤中保存图状态的 checkpoint 。
    这些检查点会保存到 thread ，在图执行后可以访问。
    由于 threads 允许在执行后访问图的状态，因此可以实现多种强大的功能，包括人工介入、记忆、时间旅行和容错性。
"""