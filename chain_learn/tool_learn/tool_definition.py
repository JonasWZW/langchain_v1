# -*- coding:utf-8 -*-
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolRuntime
from pydantic import PrivateAttr

from config import deepseek

"""
@tool 适合快速验证、简单逻辑和无状态函数；而 BaseTool 适合生产环境、有状态依赖（如数据库连接）、复杂输入校验和高度可配置的场景。
痛点一：如何优雅地管理“外部依赖”和“状态”？（Dependency Injection）
痛点二：复杂的参数校验逻辑 (Validation), 这一个其实@tool也可以
痛点三：同名工具，不同配置 (Dynamic Configuration)
class GenericSearchTool(BaseTool):
    def __init__(self, name, description, api_url, **kwargs):
        super().__init__(name=name, description=description, **kwargs)
        self.api_url = api_url
    # ... 实现逻辑使用 self.api_url

# 实例化两个完全独立的工具，互不干扰
internal_search = GenericSearchTool(
    name="internal_search", 
    description="搜内网", 
    api_url="http://internal..."
)
google_search = GenericSearchTool(
    name="google_search", 
    description="搜公网", 
    api_url="http://google..."
)

# 直接给 Agent 两个工具
tools = [internal_search, google_search]

痛点四：清晰的异步与同步分离
使用 BaseTool：
它强制你通过覆写 _run (同步) 和 _arun (异步) 两个方法来明确分离逻辑。这在代码维护上比在一个函数里通过 helper 判断要清晰得
"""


# 可以使用tool里面的参数，对工具进行详细的定义。
# 还可以使用pydantic，定义复杂的入参，让ai输入合适的参数
# 使用docstring详细的描述tool的功能
@tool()
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"


class WeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = "查询天气"

    # ✅ 私有属性：外部不可见，LLM 不可见，但实例可见
    # 不用指定PrivateAttr，也可以实现。只要使用了_或 __都可以
    # _api_key: str = PrivateAttr()
    _api_key: str

    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self._api_key = api_key  # ✅ 依赖注入：在创建时注入

    def _run(self, city: str, runtime: ToolRuntime):
        print(runtime.state)
        return f"{city}的天气是晴天"


tool_list = [search_database, WeatherTool(api_key="test_key")]

agent = create_agent(deepseek, tools=tool_list)

resp = agent.invoke({
    "messages": [
        ("human", "武汉天气如何")
    ]
})
print(resp)
