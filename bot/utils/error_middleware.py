from aiogram import BaseMiddleware
from aiogram.types import Update
from bot.utils.logger import logger

class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        try:
            return await handler(event, data)
        except Exception as e:
            # Логируем полный traceback ошибки
            logger.exception("❌ Ошибка в обработчике события!")
            
            # Если событие - это сообщение от пользователя, отправляем ему уведомление
            if isinstance(event, Update) and hasattr(event, "message"):
                await event.message.answer("⚠️ Произошла ошибка. Попробуйте ещё раз позже!")

            # Поднимаем ошибку снова, чтобы aiogram обработал её по-своему (но бот не падал)
            raise e