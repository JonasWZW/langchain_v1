# -*- coding:utf-8 -*-
"""
是什么上下文工程?
    通过一系列技术手段，使得llm能够通过context，回答出我们期望的结果。
    上下文工程是为 LLM 提供正确信息、工具，并以正确格式完成任务的上下文。
    这是 AI 工程师的首要工作。缺乏“正确”的上下文是更可靠代理的首要障碍，而 LangChain 的代理抽象设计独特，旨在促进上下文工程。


如何实现上下文工程？
    LangChain middleware is the mechanism under the hood that makes context engineering practical for developers using LangChain.
    LangChain 中间件是使 LangChain 开发人员能够实现上下文工程的底层机制。

    Middleware allows you to hook into any step in the agent lifecycle and:
    中间件允许您钩入代理生命周期的任何步骤，并：
    Update context
    更新上下文
    Jump to a different step in the agent lifecycle
    跳转到代理生命周期的不同步骤
    Throughout this guide, you’ll see frequent use of the middleware API as a means to the context engineering end.
    在整个指南中，你会频繁看到使用中间件 API 作为实现上下文工程目的的手段。

说白了就是利用中间件的能力，在model，tool侧，通过state，context，store获取用户的短暂或者持久信息，使得回答出然用户满意的答案。

model-context
    system prompt @dynamic_prompt，在不同的条件下，结合一些用户信息，state，store 调整提示词，解决相应的问题
    messages @wrap_model_call，在模型调用前，调整短暂信息和获取持久信息并注入等
    tools 详细专业的定义工具，并且@wrap_model_call的时候，帮助agent调整去除不符合条件的tools，减少上下文
    model @wrap_model_call，根据信息，动态选择合适的模型
    Response format 动态响应格式选择根据用户偏好、对话阶段或角色调整模式——在早期返回简单格式，随着复杂性的增加返回详细格式。

tool-context
    使用ToolRuntime 访问信息，然后调整修改信息（Command的update）

"""

