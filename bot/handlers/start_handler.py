from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from bot.utils.logger import logger

async def start_command(message: Message):
    """Приветственное сообщение при старте бота (Markdown V2)"""
    logger.info(f"Пользователь {message.from_user.id} запустил бота через /start")

    try:
        welcome_text = (
            "👋 *Привет\!* Я AI\-бот, который помогает с задачами и Notion\.\n\n"
            "Вот что я умею:\n"
            "📋 *\\`/tasks\\`* — показать список задач\n"
            "➕ *\\`/addtask [название]\\`* — добавить новую задачу\n"
            "💡 *\\`/ask [вопрос]\\`* — задать вопрос AI \(Qwen/GPT\)\n"
            "ℹ️ *\\`/help\\`* — показать все команды\n\n"
            "_Напиши команду, и я помогу\!_ 🚀"
        )
        await message.answer(welcome_text, parse_mode=ParseMode.MARKDOWN_V2)

    except TelegramBadRequest as e:
        logger.error(f"❌ Telegram API ошибка: {e}")
        await message.answer("⚠️ Ошибка форматирования Markdown V2\. Попробуйте позже\.", parse_mode=ParseMode.MARKDOWN_V2)

    except Exception as e:
        logger.exception("❌ Неизвестная ошибка при обработке /start!")
        await message.answer("⚠️ Произошла ошибка\. Попробуйте позже\.", parse_mode=ParseMode.MARKDOWN_V2)