# -*- coding:utf-8 -*-
"""
langgraph有两种api，graph-api，function-api。
function-api解决只想用少量代码改造，就可以使用langgraph特性。
其他情况，建议都是有graph-api

    当您需要显式控制工作流结构、复杂分支、并行处理或团队协作优势时，选择图 API。
    选择函数 API 当你想以最小的改动将 LangGraph 功能添加到现有代码中、拥有简单的线性工作流或需要快速原型设计能力。
    这两种 API 都提供了相同的 LangGraph 核心功能（持久化、流式处理、人工介入、记忆），但它们以不同的范式进行封装，以适应不同的开发风格和用例。


"""