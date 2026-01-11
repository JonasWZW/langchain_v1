"""
利用 LangGraph 掌控智能体，设计能够可靠处理复杂任务的智能体

LangGraph 专注于对代理编排至关重要的底层功能：持久执行、流式传输、人机交互等等。

langchain的底层是基于langgraph构建，langgraph使用图的数据结构来编排workflow。

node用来处理逻辑，edge用来进行路由。底层借鉴Pregel来实现工作流。

"""


"""
Thinking in LangGraph 

使用 LangGraph 构建智能体时，首先要将其分解为称为节点的离散步骤。
然后，描述每个节点的不同决策和状态转换。
最后，通过一个共享状态将节点连接起来，每个节点都可以读取和写入该状态。
"""