# -*- coding:utf-8 -*-
"""
langchain是基于langgraph进行重构的，他的底层还是基于图这一数据结构的。
node + edge  编译成 graph
中间件这个很类似于传统web开发的概念，即是在数据流在graph中流动的时候，会通过边进行路由，会在节点上进行逻辑处理，
中间件应运而生，他包裹着node，控制和自定义代理执行的每一步


中间件在每个步骤之前和之后都会暴露钩子：
    before agent
    before model
    wrap model call
    wrap tool call
    after model
    after agent

"""

"""
Best practices  最佳实践
Keep middleware focused - each should do one thing well
保持中间件的专注——每个中间件都应该做好一件事。
Handle errors gracefully - don’t let middleware errors crash the agent
优雅地处理错误——不要让中间件错误导致代理崩溃。
Use appropriate hook types:
使用合适的钩子类型 ：
Node-style for sequential logic (logging, validation)
用于顺序逻辑（日志记录、验证）的节点式编程
Wrap-style for control flow (retry, fallback, caching)
控制流（重试、回退、缓存）的包装式
Clearly document any custom state properties
清楚地记录所有自定义状态属性
Unit test middleware independently before integrating
在集成之前，对中间件进行独立的单元测试。
Consider execution order - place critical middleware first in the list
考虑执行顺序——将关键中间件放在列表的最前面
Use built-in middleware when possible
尽可能使用内置中间件
"""
