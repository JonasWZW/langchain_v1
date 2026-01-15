# -*- coding:utf-8 -*-
import asyncio
import time

from langgraph.graph import StateGraph, END
from typing import TypedDict


# 定义状态
class State(TypedDict):
    count: int
    message: str


def sync_node_a(state: State):
    print("Sync Node A: 开始请求 API (模拟)...")
    # 模拟耗时的 IO 操作，例如调用 OpenAI
    time.sleep(1)
    print("Sync Node A: API 返回")
    return {"count": state["count"] + 1, "message": "Sync A 完成"}


# 1. 定义异步节点函数
async def async_node_a(state: State):
    print("ASync Node A: 开始请求 API (模拟)...")
    # 模拟耗时的 IO 操作，例如调用 OpenAI
    await asyncio.sleep(1)
    print("ASync Node A: API 返回")
    return {"count": state["count"] + 1, "message": "ASync A 完成"}


def sync_node_b(state: State):
    print("Sync Node B: 处理数据...")
    time.sleep(1)
    return {"message": state["message"] + " ->Sync B 完成"}


async def async_node_b(state: State):
    print("Node B: 处理数据...")
    await asyncio.sleep(0.5)
    return {"message": state["message"] + " ->ASync B 完成"}


# 2. 构建图 (和同步写法完全一样)
workflow = StateGraph(State)
# workflow.add_node("node_a", async_node_a)
workflow.add_node("node_a", sync_node_a)
# workflow.add_node("node_b", sync_node_b)
workflow.add_node("node_b", sync_node_b)

workflow.set_entry_point("node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

app = workflow.compile()


# 3. 运行图 (必须使用异步入口方法)
async def main():
    inputs = {"count": 0, "message": "Start"}

    # 注意这里使用的是 ainvoke 或 astream
    # ainvoke可以调用同步的node，但是inovke不能调用async的node
    # 也就是说，如果你使用invoke，那么你的所有函数都得是同步的，不然就会TypeError
    # 因为同步的，可以被包装成async。
    # TypeError: No synchronous function provided to "node_a".
    # Either initialize with a synchronous function or invoke via the async API (ainvoke, astream, etc.)
    # During task with name 'node_a' and id '50ad29ea-66ae-dd45-c95c-0fe915b90074'

    # result = app.invoke(inputs)
    result = await app.ainvoke(inputs)
    print(f"最终结果: {result}")


# 在 Python 环境中运行
# import asyncio
asyncio.run(main())
