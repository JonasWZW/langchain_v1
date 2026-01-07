# -*- coding:utf-8 -*-
from config import deepseek
import asyncio
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 设置 Chain
model = deepseek
prompt = ChatPromptTemplate.from_template("50字简短解释下什么是: {concept}")
output_parser = StrOutputParser()

chain = prompt | model | output_parser


# --- 同步部分 ---
def sync_examples():
    print("=== 同步调用开始 ===")

    # 1. Invoke
    resp1 = chain.invoke({'concept': 'LCEL'})
    print(f"1. Invoke: {resp1}")

    # 2. Stream
    print("2. Stream: ", end="")
    for chunk in chain.stream({'concept': 'Stream'}):
        print(chunk, end="", flush=True)
    print()

    # 3. Batch
    print("3. Batch: 开始...")
    start = time.time()
    res = chain.batch([{'concept': 'Apple'}, {'concept': 'Banana'}])
    print(f"   耗时: {time.time() - start:.2f}s, 结果数: {len(res)}")


# --- 异步部分 ---
async def async_examples():
    print("\n=== 异步调用开始 ===")

    # 1. Ainvoke
    res = await chain.ainvoke({'concept': 'Asyncio'})
    print(f"1. Ainvoke: {res}")

    # 2. Astream
    print("2. Astream: ", end="")
    async for chunk in chain.astream({'concept': 'WebSocket'}):
        print(chunk, end="", flush=True)
    print()

    # 3. Abatch
    print("3. Abatch: 开始...")
    start = time.time()
    res = await chain.abatch([{'concept': 'Docker'}, {'concept': 'K8s'}])
    print(f"   耗时: {time.time() - start:.2f}s, 结果: {res}")


if __name__ == "__main__":
    # 运行同步
    sync_examples()

    # 运行异步
    asyncio.run(async_examples())
