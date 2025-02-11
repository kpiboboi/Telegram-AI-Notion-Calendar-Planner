from openai import OpenAI  # из пакета dashscope
from bot.config import DASHSCOPE_API_KEY, QWEN_BASE_URL, QWEN_MODEL

from bot.utils.logger import logger

def qwen_chat(messages):
    logger.debug("Отправляем запрос к Qwen...")
    try:
        client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=QWEN_BASE_URL)
        completion = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=messages
        )
        logger.debug("Ответ получен успешно.")
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка при вызове Qwen: {e}")
        return "Извините, не могу ответить."