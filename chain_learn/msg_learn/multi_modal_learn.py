# -*- coding:utf-8 -*-
from langchain.chat_models import init_chat_model

from config import BASE_URL, API_KEY


# chat model 找不到
# openai.BadRequestError: Error code: 400 - {'code': 20012, 'message': 'Model does not exist. Please check it carefully.', 'data': None}
qwen_image = init_chat_model(
    "Qwen/Qwen-Image-Edit-2509",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=1
)
resp = qwen_image.invoke("帮我生产一个猫咪的图片")

print(resp.content_blocks)