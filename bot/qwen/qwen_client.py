from openai import OpenAI  # из пакета dashscope
from bot.config import DASHSCOPE_API_KEY, QWEN_BASE_URL, QWEN_MODEL

def qwen_chat(messages):
    client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=QWEN_BASE_URL)
    completion = client.chat.completions.create(
        model=QWEN_MODEL,
        messages=messages
    )
    return completion.choices[0].message.content