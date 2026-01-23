import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


# 1. 定义状态
class State(TypedDict):
    # 使用 reducer 来合并并行节点的结果
    results: Annotated[list, operator.add]


# 2. 定义并行节点
# 注意：这三个节点在同一个 Super-step 中并行运行

def node_a(state):
    print("--- [A] 正在运行，准备中断 ---")

    # 【关键点】：interrupt 会暂停。
    # 当恢复时，resume_value 将是用户传进来的那个大字典
    resume_value = interrupt("Node A 需要输入")
    # 因为大家收到的是同一个字典，所以要按 Key 取值
    my_input = resume_value.get("a_input")
    print(f"--- [A] 恢复成功，收到: {my_input} ---")

    resume_value2 = interrupt("Node A 需要输入2")
    my_input2 = resume_value2.get("a_input2")
    print(f"--- [A] 恢复成功，收到: {my_input2} ---")
    return {"results": [f"A说: {my_input} + {my_input2}"]}


def node_b(state):
    print("--- [B] 正在运行，准备中断 ---")

    resume_value = interrupt("Node B 需要输入")
    my_input = resume_value.get("b_input")

    print(f"--- [B] 恢复成功，收到: {my_input} ---")
    return {"results": [f"B说: {my_input}"]}


def node_c(state):
    print("--- [C] 正在运行，准备中断 ---")

    resume_value = interrupt("Node C 需要输入")
    my_input = resume_value.get("c_input")

    print(f"--- [C] 恢复成功，收到: {my_input} ---")
    return {"results": [f"C说: {my_input}"]}


# 3. 构建图
builder = StateGraph(State)

builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)

builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", "node_c")

builder.add_edge("node_c", END)

# 必须配置 Checkpointer 才能使用 interrupt
checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# --- 实验开始 ---

# 线程配置 ID
config = {"configurable": {"thread_id": "test_parallel_interrupt"}}

print("========= 第一阶段：启动图，触发并行中断 =========")
# 第一次运行
initial_input = {"results": []}

# 使用 stream 运行，直到被 interrupt 打断
resp1 = app.invoke(initial_input, config)

print("\n(图已经暂停。现在你可以去检查 State，或准备恢复)")

# 查看当前状态，确认有 3 个任务在等待
current_state1 = app.get_state(config)
print(f"当前等待的任务数量: {len(current_state1.tasks)}")
print(f"下一步待执行节点: {current_state1.next}")

print("\n========= 第二阶段：构造数据并恢复 =========")

# 【核心逻辑】：
# 既然有3个节点都在等，我们就构造一个包含 3 份答案的字典。
# 当我们调用 resume 时，这个字典会被发送给 A、B、C 三个节点。
user_input_payload = {
    "a_input": "你好 A",
    "a_input2": "jonas",
    "b_input": "你好 B",
    "c_input": "你好 C"
}

print(f"我传入的 Resume 数据: {user_input_payload}")
print("正在恢复执行...\n")

# 使用 Command 对象进行恢复
# 注意：resume 的值就是上面的 payload

# 恢复A
resp2 = app.invoke(Command(resume=user_input_payload), config)
current_state2 = app.get_state(config)
print(f"当前等待的任务数量: {len(current_state2.tasks)}")
print(f"下一步待执行节点: {current_state2.next}")

resp2 = app.invoke(Command(resume=user_input_payload), config)
current_state2 = app.get_state(config)
print(f"当前等待的任务数量: {len(current_state2.tasks)}")
print(f"下一步待执行节点: {current_state2.next}")

# 恢复B
resp3 = app.invoke(Command(resume=user_input_payload), config)
current_state3 = app.get_state(config)
print(f"当前等待的任务数量: {len(current_state3.tasks)}")
print(f"下一步待执行节点: {current_state3.next}")

# 恢复C
resp4 = app.invoke(Command(resume=user_input_payload), config)
current_state4 = app.get_state(config)
print(f"当前等待的任务数量: {len(current_state4.tasks)}")
print(f"下一步待执行节点: {current_state4.next}")

print("\n========= 最终结果 =========")
print(resp4)
