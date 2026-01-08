"""
如何定义中间件？
本质其就是继承 AgentMiddleware
或者使用装饰器进行处理
说白了就是实现相对应钩子的逻辑即可
    
    before agent
    before model
    after model
    after agent


    wrap model call
    wrap tool call

Built-in middleware  内置中间件
针对常见代理用例的预构建中间件
LangChain 为常见用例提供预构建的中间件。每个中间件都已准备好投入生产环境，并且可以根据您的特定需求进行配置。
内置中间件都是官方很好的实现，如果我们自己不会写自定义的中间件，完全可以参考官方给出的内置中间件。

如何隔离不同thread_id下的短期记忆，或者说如何对于继承AgentMiddleware的中间件，有自己的私有的变量？
核心： AgentState是个dict，随便咱们扩展。

class ModelCallLimitMiddleware(AgentMiddleware[ModelCallLimitState, Any]):
    state_schema = ModelCallLimitState

class ModelCallLimitState(AgentState):
    thread_model_call_count: NotRequired[Annotated[int, PrivateStateAttr]]
    run_model_call_count: NotRequired[Annotated[int, UntrackedValue, PrivateStateAttr]]

"""
