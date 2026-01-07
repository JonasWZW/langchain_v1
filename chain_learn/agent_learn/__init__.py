# -*- coding:utf-8 -*-
"""
create_agent 使用 LangGraph 构建基于图的代理运行时。
图由节点（步骤）和边（连接）组成，定义了代理处理信息的方式。
代理在图中移动，执行节点，如模型节点（调用模型）、工具节点（执行工具）或中间件。
"""

"""
1 模型
2 tool
3 提示词

4 调用？
invoke
stream
batch
async?
5 结构化输出
structured output
6 短期记忆
memory(short-term-memory)
7 长期记忆
store(long-term-memory)
8 中间件
middleware
"""