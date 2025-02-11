import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime

from openai import OpenAI

load_dotenv(dotenv_path="bot/.env")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL")
QWEN_MODEL = os.getenv("QWEN_MODEL")
CHAT_DATABASE_ID = os.getenv("NOTION_CHAT_DB")

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

# Команда /start
@dp.message(Command("start"))
async def send_start(message: Message):
    help_text = (
        "Privet eto bot Notion planner AI assitent\n"
        "/help - Показать список команд"
    )
    await message.answer(help_text)

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

def qwen_chat(messages):
    """
    Отправляет список сообщений в Qwen и возвращает ответ.
    messages - формат: [{"role": "user", "content": "..."}, ...]
    """
    client = OpenAI(
        api_key=DASHSCOPE_API_KEY,
        base_url=QWEN_BASE_URL,
    )
    # Создаём чатовое завершение
    completion = client.chat.completions.create(
        model=QWEN_MODEL,
        messages=messages
    )
    # Возвращаем текстовое содержание ответа
    return completion.choices[0].message.content


# Команда /ask — пользователь задаёт любой вопрос к Qwen
@dp.message(Command("ask"))
async def handle_ask(message: Message):
    user_input = message.text.replace("/ask", "").strip()
    if not user_input:
        await message.answer("Введите вопрос после команды /ask")
        return

    # Формируем список сообщений для Qwen
    # Можно добавить "system" роль, если нужна контекстная инструкция
    messages = [
        {"role": "system", "content": "You are a helpful AI Assistant."},
        {"role": "user", "content": user_input}
    ]

    # Вызываем Qwen для получения ответа
    answer = qwen_chat(messages)
    await message.answer(answer)


async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())