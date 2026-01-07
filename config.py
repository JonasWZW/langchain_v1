from dotenv import load_dotenv
import os

from langchain.chat_models import init_chat_model

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
print(BASE_URL, API_KEY)

deepseek = init_chat_model(
    "deepseek-ai/DeepSeek-V3",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=1
)


deepseek_r1 = init_chat_model(
    "deepseek-ai/DeepSeek-R1",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=1
)