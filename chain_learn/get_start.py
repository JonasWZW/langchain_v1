from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

from config import BASE_URL, API_KEY, deepseek

if __name__ == '__main__':
    resp = deepseek.invoke([
        ("user", "50字介绍神经网络")
    ])
    print(type(resp))
    print(resp)
