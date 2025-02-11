from aiogram.types import Message
from aiogram.filters import Command
from bot.notion.tasks import get_tasks, add_task

async def tasks_command(message: Message):
    tasks_list = get_tasks()  # Возвращает [(name, status), ...]
    if tasks_list:
        response = "\n".join([f"🔹 {t[0]} — {t[1]}" for t in tasks_list])
    else:
        response = "Нет задач для отображения."
    await message.answer(f"📋 **Список задач:**\n{response}")

async def addtask_command(message: Message):
    task_name = message.text.replace("/addtask", "").strip()
    if not task_name:
        await message.answer("❗ Пожалуйста, укажите название задачи.")
        return

    add_task(task_name)
    await message.answer(f"✅ Задача '{task_name}' добавлена в таблицу Notion.")