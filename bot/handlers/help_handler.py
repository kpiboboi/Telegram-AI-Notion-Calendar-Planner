from aiogram.types import Message
from aiogram.filters import Command

async def help_command(message: Message):
    help_text = (
        "/tasks - Показать краткий список задач\n"
        "/addtask [название] - Добавить новую задачу\n"
        "/ask [вопрос] - Спросить Qwen\n"
        "/help - Показать список команд"
    )
    await message.answer(help_text)