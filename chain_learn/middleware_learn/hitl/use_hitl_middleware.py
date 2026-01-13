"""
想要实现HITL功能，需要你实例化一个中间件，然后对该中间件进行配置，然后create_agent的时候传入

"""

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware.human_in_the_loop import HITLResponse, ApproveDecision
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from config import deepseek


@tool
def write_file():
    """read data to file

    """
    print("write_file_tool")


@tool
def execute_sql():
    """execute sql

    """
    print("execute_sql_tool")


@tool
def read_data():
    """read data from files

    """
    print("read_data_tool")


agent = create_agent(
    model=deepseek,
    tools=[write_file, execute_sql, read_data],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,  # All decisions (approve, edit, reject) allowed
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
                "read_data": False,
            },
            description_prefix="Tool execution pending approval",
        ),
    ],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "some_id"}}
# Run the graph until the interrupt is hit.
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "执行write_file和execute_sql工具",
            }
        ]
    },
    config=config
)

print(result["__interrupt__"])
"""
[Interrupt(
value={'action_requests': [{'name': 'write_file', 'args': {}, 'description': 'Tool execution pending approval Tool: write_file Args: {}'}], 
'review_configs': [{'action_name': 'write_file', 'allowed_decisions': ['approve', 'edit', 'reject']}]}, 
id='98fae3ae5c93eb07c3cb3948aad47c21')]



class HITLRequest(TypedDict):
    action_requests: list[ActionRequest]
    review_configs: list[ReviewConfig]

[Interrupt(value={
    'action_requests': [
        {'name': 'write_file', 'args': {}, 'description': 'Tool execution pending approval\n\nTool: write_file\nArgs: {}'}, 
        {'name': 'execute_sql', 'args': {}, 'description': 'Tool execution pending approval\n\nTool: execute_sql\nArgs: {}'}
        ], 
    'review_configs': [
        {'action_name': 'write_file', 'allowed_decisions': ['approve', 'edit', 'reject']}, 
        {'action_name': 'execute_sql', 'allowed_decisions': ['approve', 'reject']}
        ]
}, 
id='cc510ba1c557e5d42f9ad65d2a3e1146')]

"""
# 有可能result["__interrupt__"]返回的是一个list，里面可能有多个Interrupt对象，
# 那么返回的的Command的resume的需要和Interrupt按照顺序一一对应
# 什么场景会出现？ langgraph的时候，一个super-step分出去多个node执行？其中多个node都会interrupt？
# Resume with approval decision
"""
Decision = ApproveDecision | EditDecision | RejectDecision

class HITLResponse(TypedDict):
    decisions: list[Decision]

前端的时候，需要一次按照HITLRequest的内容和中断的返回项，传递给用户，
用户自己选择。
    例如： AI想要调用write_file，参数是args，你是否允许？['approve', 'edit', 'reject']. 选择不同的操作，返回不同的 HITLResponse就好了。
"""

agent.invoke(
    # Command(
    #     resume={"decisions": [
    #         {"type": "approve"},
    #         {"type": "approve"}
    #     ]}  # or "reject"
    # ),
    Command(
        resume=HITLResponse(decisions=[ApproveDecision(type='approve'), ApproveDecision(type='approve')])
    ),
    config=config  # Same thread ID to resume the paused conversation
)
# 如果没有管中断点，直接继续调用，中断点不会执行。相应的逻辑会跳过
# result = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "执行read_data工具",
#             }
#         ]
#     },
#     config=config
# )
# print(result)
"""
详细逻辑可以查看HumanInTheLoopMiddleware的源码，底层就是使用interrupt+middleware(after_model_call)实现的

Execution lifecycle  执行生命周期
The middleware defines an after_model hook that runs after the model generates a response but before any tool calls are executed:
中间件定义了一个 after_model 钩子，该钩子在模型生成响应之后、任何工具调用执行之前运行：
The agent invokes the model to generate a response.
代理调用模型生成响应。
The middleware inspects the response for tool calls.
中间件会检查响应中是否存在工具调用。
If any calls require human input, the middleware builds a HITLRequest with action_requests and review_configs and calls interrupt.
如果任何调用需要人工输入，中间件会构建一个包含 action_requests 和 review_configs 的 HITLRequest ，并调用 interrupt 。
The agent waits for human decisions.
智能体等待人类做出决定。
Based on the HITLResponse decisions, the middleware executes approved or edited calls, synthesizes ToolMessage’s for rejected calls, and resumes execution.
根据 HITLResponse 决定，中间件执行已批准或已编辑的调用，合成被拒绝调用的 ToolMessage ，并恢复执行。
"""
