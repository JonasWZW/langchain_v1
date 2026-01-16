# -*- coding:utf-8 -*-
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from typing import Annotated

from langgraph.types import StateSnapshot
from typing_extensions import TypedDict
from operator import add


class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]


def node_a(state: State):
    print(f"node a --> {state}")
    return {"foo": "a", "bar": ["a"]}


def node_b(state: State):
    print(f"node b --> {state}")
    return {"foo": "b", "bar": ["b"]}


def wzw_node(state: State):
    print(f"wzw_node --> {state}")
    return None


workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_node(wzw_node)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
resp = graph.invoke({"foo": "", "bar": []}, config)
print(resp)
print("----------------------------")

last_snapshot = graph.get_state(config)
print(last_snapshot)
print("----------------------------")
all_snapshot = list(graph.get_state_history(config))
for item in all_snapshot:
    print(item)
    print()
print("----------------------------")
cfg = all_snapshot[2].config
cfg_snapshot = graph.get_state(cfg)
print(cfg)
print(cfg_snapshot)
print("----------------------------")
# 这里没有发生replay，说明replay的时候，必须input为None
# 没有replay就是调用了两次，一共8个StateSnapshot
# resp = graph.invoke({"foo": "wzw", "bar": ["football", "tennis"]}, config=cfg)
# 最后获取history state，replay有4+2个StateSnapshot
resp = graph.invoke(None, config=cfg)
print(resp)
print("----------------------------")
all_snapshot = list(graph.get_state_history(config))
for item in all_snapshot:
    print(item)
    print()
print("----------------------------")
last_cfg = all_snapshot[4].config
fork_last_cfg = graph.update_state(config=last_cfg, values={"foo": "wzw", "bar": ["wzw"]})
# todo fork_last_cfg的parent_config checkpoint_id指向 last_cfg的checkpoint_id
print(last_cfg)
print(fork_last_cfg)
resp = graph.invoke(None, fork_last_cfg)
print(resp)
print("----------------------------")
all_snapshot = list(graph.get_state_history(config))
for item in all_snapshot:
    print(item)
    print()
print("----------------------------")
# todo replay的时候，是从checkpoint id和parent_config一样的节点开始。update_state是就是和checkpoint id相等的节点开始。