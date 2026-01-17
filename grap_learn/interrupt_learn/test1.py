import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


# 1. 定义状态
class State(TypedDict):
    results: Annotated[list, operator.add]


# 2. 定义并行节点
# 注意：现在节点不需要自己去拆解字典了，它会直接收到属于它的那个值
def node_a(state):
    print("--- [A] 正在运行，准备中断 ---")
    # 这里的 user_input 就会直接是 "你好 A"
    user_input = interrupt("Node A 请输入")
    print(f"--- [A] 恢复成功，收到: {user_input} ---")
    return {"results": [f"A收到: {user_input}"]}


def node_b(state):
    print("--- [B] 正在运行，准备中断 ---")
    user_input = interrupt("Node B 请输入")
    print(f"--- [B] 恢复成功，收到: {user_input} ---")
    return {"results": [f"B收到: {user_input}"]}


def node_c(state):
    print("--- [C] 正在运行，准备中断 ---")
    user_input = interrupt("Node C 请输入")
    print(f"--- [C] 恢复成功，收到: {user_input} ---")
    return {"results": [f"C收到: {user_input}"]}


# 3. 构建图
builder = StateGraph(State)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)
builder.add_edge(START, "node_a")
builder.add_edge(START, "node_b")
builder.add_edge(START, "node_c")
builder.add_edge("node_a", END)
builder.add_edge("node_b", END)
builder.add_edge("node_c", END)

checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# --- 实验开始 ---

config = {"configurable": {"thread_id": "test_fixed_parallel"}}
initial_input = {"results": []}

print("========= 1. 启动图，触发并行中断 =========")
# 运行直到所有节点都中断
for event in app.stream(initial_input, config):
    pass

print("\n(图已暂停，正在准备恢复数据...)\n")

# ========= 关键修正部分开始 =========

# 1. 获取当前状态
snapshot = app.get_state(config)

# 2. 准备我们要输入的数据 (模拟前端收集到的用户输入)
user_responses = {
    "node_a": "我是A的答案",
    "node_b": "我是B的答案",
    "node_c": "我是C的答案"
}

# 3. 动态构建 resume 字典： { interrupt_id : value }
resume_payload = {}

# snapshot.tasks 包含了当前所有挂起的任务
for task in snapshot.tasks:
    # task.name 是节点名称，例如 "node_a"
    node_name = task.name

    # task.interrupts 是该任务下的中断列表 (通常只有一个)
    if task.interrupts:
        # 获取第一个中断对象
        interrupt_item = task.interrupts[0]
        interrupt_id = interrupt_item.id  # 获取系统生成的唯一 ID

        # 找到我们要给这个节点的值
        if node_name in user_responses:
            print(f"匹配成功: 节点[{node_name}] -> ID[{interrupt_id}] -> 值[{user_responses[node_name]}]")
            # 【核心】：将 ID 映射到具体的值
            resume_payload[interrupt_id] = user_responses[node_name]

print(f"\n构造的 Resume Payload: {resume_payload}\n")
print("========= 2. 恢复执行 =========")

# 4. 使用构造好的 ID 字典进行恢复
# 注意：stream 内部会自动根据 ID 分发数据
"""
构造的 Resume Payload: {'85fc8db6837fcb895033906cd59a181e': '我是A的答案', '899787bb68a475385d651c1ae834cf36': '我是B的答案', 'ca75ac9db0183431e6c0c48507cc101c': '我是C的答案'}

        resume: Value to resume execution with. To be used together with [`interrupt()`][langgraph.types.interrupt].
            Can be one of the following:
            - Mapping of interrupt ids to resume values
            - A single value with which to resume the next interrupt
"""
for event in app.stream(Command(resume=resume_payload), config):
    pass

print("\n========= 最终结果 =========")
final_state = app.get_state(config)
print(final_state.values["results"])