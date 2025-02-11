from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.utils.logger import logger

class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        """
        Перехватывает вызов хендлера. Если в хендлере возникает ошибка,
        мы её логируем и можем отреагировать (например, сообщить пользователю).
        """
        try:
            return await handler(event, data)
        except Exception as e:
            # Логируем traceback
            logger.exception("Произошла ошибка в обработчике события!")
            
            # Если нужно, можно ответить пользователю об ошибке:
            # Пример: если это объект Message, можем отправить в тот же чат
            if hasattr(event, "reply") and callable(event.reply):
                await event.reply("Упс, произошла ошибка. Попробуйте позже!")
            
            # Пробрасываем ошибку дальше или "глушим" её.
            raise e
