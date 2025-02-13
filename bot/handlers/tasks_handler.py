from aiogram.types import Message
from bot.notion.tasks import get_tasks, add_task
from bot.utils.logger import logger
from aiogram.enums import ParseMode


async def tasks_command(message: Message):
    #Выводит список задач из Notion
    logger.info(f"Пользователь {message.from_user.id} вызвал /tasks")
    try:
        tasks_list = await get_tasks()
        if tasks_list:
            response = "\n".join([f"🔹 {t[0]} ➖ {t[1]}" for t in tasks_list])
            logger.debug(f"Отправляем {len(tasks_list)} задач.")
        else:
            logger.debug("Задач не найдено.")
            response = "Нет задач для отображения."
    except Exception as e:
        logger.exception("❌ Ошибка при получении задач из Notion!")
        response = "⚠️ Произошла ошибка при получении задач."

    tasklist = (f"📋 <b>Список задач:</b>\n{response}")
    await message.answer(tasklist, parse_mode=ParseMode.HTML)

async def addtask_command(message: Message):
    #Добавляет задачу в Notion
    logger.info(f"Пользователь {message.from_user.id} вызвал /addtask")
    task_name = message.text.replace("/addtask", "").strip()

    if not task_name:
        logger.debug("Название задачи пусто.")
        await message.answer("❗ Пожалуйста, укажите название задачи.")
        return

    try:
        await add_task(task_name)
        logger.debug(f"Задача '{task_name}' добавлена.")
        await message.answer(f"✅ Задача '{task_name}' добавлена в таблицу Notion.")
    except Exception as e:
        logger.exception("❌ Ошибка при добавлении задачи в Notion!")
        await message.answer("⚠️ Не удалось добавить задачу. Попробуйте позже.")