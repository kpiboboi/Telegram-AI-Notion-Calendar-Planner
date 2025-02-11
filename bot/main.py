import asyncio
from aiogram import Bot, Dispatcher
from bot.config import API_TOKEN
from bot.handlers.tasks_handler import tasks_command, addtask_command
from bot.handlers.help_handler import help_command
from bot.handlers.qwen_handler import ask_command

def register_handlers(dp: Dispatcher):
    from aiogram.filters import Command
    dp.message.register(help_command, Command("help"))
    dp.message.register(tasks_command, Command("tasks"))
    dp.message.register(addtask_command, Command("addtask"))
    dp.message.register(ask_command, Command("ask"))

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Регистрируем все хендлеры
    register_handlers(dp)

    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())