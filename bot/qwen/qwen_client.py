from openai import AsyncOpenAI
from bot.config import DASHSCOPE_API_KEY, QWEN_BASE_URL, QWEN_MODEL
from bot.utils.logger import logger

async def qwen_chat(messages_list):

    logger.debug("Отправляем запрос к Qwen...")
    try:
        client = AsyncOpenAI(api_key=DASHSCOPE_API_KEY, base_url=QWEN_BASE_URL)
        completion = await client.chat.completions.create(
            model=QWEN_MODEL,
            messages=messages_list
        )
        logger.debug("Ответ получен успешно.")
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка при вызове Qwen: {e}")
        return "Извините, не могу ответить."