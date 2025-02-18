import asyncio
import logging # for detail loogging
from aiogram import Bot, Dispatcher

from bot.config import API_TOKEN
from bot.utils.logger import logger
from bot.handlers.tasks_handler import tasks_command, addtask_command
from bot.handlers.start_handler import start_command
from bot.handlers.help_handler import help_command
from bot.handlers.qwen_handler import ask_command
from bot.utils.error_middleware import ErrorMiddleware
from bot.handlers.schedule_handler import schedule_command
from bot.handlers.schedule_handler import router as schedule_router



def register_handlers(dp: Dispatcher):
    from aiogram.filters import Command
    dp.message.register(start_command, Command("start"))
    dp.message.register(help_command, Command("help"))
    dp.message.register(tasks_command, Command("tasks"))
    dp.message.register(addtask_command, Command("addtask"))
    dp.message.register(ask_command, Command("ask"))
    dp.message.register(schedule_command, Command("schedule"))
    dp.include_router(schedule_router)

async def main():
    logging.basicConfig(level=logging.INFO) # for detail logging only
    logger.info("🚀 Бот запущен!")

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.update.middleware(ErrorMiddleware())
    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.warning("❌ Бот остановлен пользователем.")
    finally:
        logger.info("🛑 Завершаем работу бота...")
        await bot.session.close()
        logger.info("✅ Бот корректно завершил работу.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("❌ Выход из приложения по Ctrl+C.")