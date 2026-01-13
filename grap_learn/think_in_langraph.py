# -*- coding:utf-8 -*-

"""
使用 LangGraph 构建智能体时，
    你首先需要将其分解为称为节点的独立步骤。
    然后，你需要描述每个节点之间的不同决策和转换。
    最后，通过一个共享状态连接节点，每个节点都可以从中读取和写入。

说白了，就是三个方面，划分每个节点应该做什么？节点之间怎么链接？需要什么样子的共享状态在节点中流转？
"""

"""
langgraph的官方样例，写邮件

需求：
    The agent should:
    - Read incoming customer emails
    - Classify them by urgency and topic
    - Search relevant documentation to answer questions
    - Draft appropriate responses
    - Escalate complex issues to human agents
    - Schedule follow-ups when needed
    
    Example scenarios to handle:
    
    1. Simple product question: "How do I reset my password?"
    2. Bug report: "The export feature crashes when I select PDF format"
    3. Urgent billing issue: "I was charged twice for my subscription!"
    4. Feature request: "Can you add dark mode to the mobile app?"
    5. Complex technical issue: "Our API integration fails intermittently with 504 errors"


分解node，定义每个node应该做什么？
    Read Email : 提取并解析邮件内容
    Classify Intent : 使用 LLM 对紧急程度和主题进行分类，然后路由到适当的操作
    Doc Search : 查询知识库以获取相关信息
    Bug Track : 在跟踪系统中创建或更新问题
    Draft Reply : 生成适当的回复
    Human Review : 升级至人工代理以获得批准或处理
    Send Reply : 发送邮件响应

节点之间如何链接？
    graph_connect.png
    其中，虚线代表可以选择的，实线代表必定的链接。
    
这个时候，我们定义了node应该做什么，node之间如何链接，现在我们需要定义state，特别是进入某的node，他需要state中的什么数据，他是否又应该给state提供新的数据？
其次，对于node的具体实现，我们应该进行划分：
    LLM node 当步骤需要理解、分析、生成文本或做出推理决策时：
    tool node 需要扩展graph的能力的
        data node 当一个步骤需要从外部来源检索信息时（read）： 
            1，我们直接依据一些状态信息读取到外部的数据。2，我们可以把获取数据的能力包装成tool让llm自己获取
            通常来说，如果逻辑确定，使用第一种比较好，因为编码的形式比较稳定，不容易出错，也节省了一次llm调用
        action node（tool） 当一个步骤需要执行外部操作时（write）：
            1，我们根据ai的生成+tool，进行数据的保存。2，我们提供llm延申的能力，进行外界的交互。
    human-in-the-loop node 当一个步骤需要人工干预时：

对于state的设定，遵循一些原则：
    它需要跨步骤持久化吗？如果需要，就放在状态中（也就是说这个信息，后续的node也会使用）。
    你能从其他数据中推导出它吗？如果可以，在需要时计算它，而不是存储在状态中（如果计算代价大，可以直接保存在state）。
    一个关键原则：你的状态应该存储原始数据，而不是格式化的文本。在需要时，在节点内部格式化提示。
    
node的本质，是一个个函数，它接受当前状态并返回对状态的更新。
那么一个函数，就有可能发生异常，我们需要对其进行分类和处理（不要让某个异常导致程序崩溃）：

    1，Transient errors (network issues, rate limits)
        加个重试机制就行了
        from langgraph.types import RetryPolicy
        workflow.add_node(
            "search_documentation",
            search_documentation,
            retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0)
        )
    
    2，LLM-recoverable errors (tool failures, parsing issues) ToolNode这个预构建几乎都做到了
        捕获异常，返回一个ToolMessage里面的内容是异常的信息，让llm自己调整
    
    3，User-fixable errors (missing information, unclear instructions)
        在需要时暂停并从用户那里收集信息（例如账户 ID、订单号或澄清）：
        from langgraph.types import Command
        def lookup_customer_history(state: State) -> Command[Literal["draft_response"]]:
            if not state.get('customer_id'):
                user_input = interrupt({
                    "message": "Customer ID needed",
                    "request": "Please provide the customer's account ID to look up their subscription history"
                })
                return Command(
                    update={"customer_id": user_input['customer_id']},
                    goto="lookup_customer_history"
                )
            # Now proceed with the lookup
            customer_data = fetch_customer_history(state['customer_id'])
            return Command(update={"customer_history": customer_data}, goto="draft_response")
        
    4，Unexpected errors
        直接raise出去，暴露出去
"""
