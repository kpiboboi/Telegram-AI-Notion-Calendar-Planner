from aiogram.types import Message
from aiogram.filters import Command
from bot.qwen.qwen_client import qwen_chat

from bot.utils.logger import logger

async def ask_command(message: Message):
    logger.info(f"Пользователь {message.from_user.id} вызвал /ask")
    user_input = message.text.replace("/ask", "").strip()
    if not user_input:
        logger.debug("Список задач пуст.")
        await message.answer("Введите вопрос после команды /ask")
        return

    # Формируем список сообщений
    messages = [
        {"role": "system", "content": "You are a helpful AI Assistant."},
        {"role": "user", "content": user_input}
    ]
    answer = qwen_chat(messages)
    await message.answer(answer)