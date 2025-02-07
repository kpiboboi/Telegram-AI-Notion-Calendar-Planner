from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="bot/.env")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
notion = Client(auth=NOTION_TOKEN)

# Получаем задачи из Notion
async def get_tasks():
    results = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "sorts": [
                {"property": "Prioritet", "direction": "ascending"}
            ]
        }
    )
    tasks = [f"🔹 {task['properties']['Ishlar']['title'][0]['text']['content']} — {task['properties']['Holat']['select']['name']}" for task in results['results']]
    return tasks

# Команда /tasks — показать краткий список задач
@dp.message(Command("tasks"))
async def send_tasks(message: Message):
    tasks = await get_tasks()
    response = "\n".join(tasks) if tasks else "Нет задач для отображения."
    await message.answer(f"📋 **Список задач:**\n{response}")

# Команда /help — показать доступные команды
@dp.message(Command("help"))
async def send_help(message: Message):
    help_text = (
        "/tasks - Показать краткий список задач\n"
        "/fulltable - Показать полную таблицу задач\n"
        "/addtask [название задачи] - Добавить новую задачу\n"
        "/help - Показать список команд"
    )
    await message.answer(help_text)

# Обработчик команды /addtask для добавления задачи
@dp.message(Command("addtask"))
async def add_task(message: Message):
    task_name = message.text.replace("/addtask", "").strip()
    if not task_name:
        await message.answer("❗ Пожалуйста, укажите название задачи.")
        return

    # Добавляем задачу в Notion
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Ishlar": {"title": [{"text": {"content": task_name}}]},
            "Holat": {"select": {"name": "Boshlanmadi"}},  # По умолчанию статус "Не начата"
        }
    )
    await message.answer(f"✅ Задача '{task_name}' добавлена в таблицу Notion.")

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())