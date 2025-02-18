import re
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.notion.notion_api import NotionAPI
from bot.config import DATABASE_ID, SCHEDULE_DATABASE_ID
from bot.utils.logger import logger
from bot.qwen.qwen_client import qwen_chat
from datetime import datetime

router = Router()
notion_tasks_api = NotionAPI()
notion_schedule_api = NotionAPI()

@router.message(Command("schedule"))
async def schedule_command(message: Message):
    try:
        tasks_data = await load_tasks_from_notion()
        if not tasks_data:
            await message.answer("Нет актуальных задач для планирования.")
            return

        prompt = build_schedule_prompt(tasks_data)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        schedule_text = await qwen_chat(messages)
        logger.info(f"GPT ответ:\n{schedule_text}")

        parsed_schedule = parse_gpt_schedule(schedule_text)
        if not parsed_schedule:
            await message.answer("GPT не смог сгенерировать расписание.")
            return

        await write_schedule_to_notion(parsed_schedule)
        result_msg = "Расписание на сегодня:\n" + schedule_text
        await message.answer(result_msg)
    except Exception as e:
        logger.error(f"Ошибка при формировании расписания: {e}")
        await message.answer("Произошла ошибка при составлении расписания.")

async def load_tasks_from_notion():
    filter_obj = {
        "filter": {
            "or": [
                {"property": "Holat", "select": {"equals": "Boshlanmadi"}},
                {"property": "Holat", "select": {"equals": "Jarayonda"}}
            ]
        },
        "sorts": [
            {"property": "Prioritet", "direction": "ascending"},
            {"property": "Deadline", "direction": "ascending"}
        ]
    }

    response = await notion_tasks_api.query_database(DATABASE_ID, filter_obj)
    tasks = []
    for item in response["results"]:
        props = item["properties"]

        name = props["Ishlar"].get("title", [{}])[0].get("text", {}).get("content", "Без названия")
        priority = props.get("Prioritet", {}).get("select", {}).get("name", "P3")
        status = props.get("Holat", {}).get("select", {}).get("name", "Jarayonda")
        deadline = props.get("Deadline", {}).get("date", {}).get("start", None)

        tasks.append({
            "name": name,
            "priority": priority,
            "status": status,
            "deadline": deadline
        })
    return tasks

def build_schedule_prompt(tasks_data):
    prompt = "Ты — умный планировщик. У меня есть задачи:\n"
    for t in tasks_data:
        prompt += f"- {t['name']} (Приоритет: {t['priority']}, Статус: {t['status']}"
        if t['deadline']:
            prompt += f", Дедлайн: {t['deadline']}"
        prompt += ")\n"

    prompt += (
        "\nСоставь расписание на сегодня (09:00–18:00), "
        "указывая время начала и окончания каждой задачи. "
        "Формат вывода: '09:00–10:00: Название задачи (P1)'. "
        "\nУчти приоритет: Если задача P1, ставь раньше. P2 – средний. P3 – низкий. "
        "Если задач много, P1 получат время в первую очередь."
    )
    return prompt

def parse_gpt_schedule(schedule_text):
    pattern = re.compile(r"^(\d{2}:\d{2})-(\d{2}:\d{2}):\s*(.*)$")
    lines = schedule_text.split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        line = re.sub(r"[–—]+", "-", line)
        m = pattern.match(line)
        if not m:
            logger.warning(f"Не удалось распознать строку: {line}")
            continue

        start_time = m.group(1)
        end_time = m.group(2)
        task_part = m.group(3).strip()

        priority = "P3"
        if "(" in task_part and ")" in task_part:
            try:
                name_part, prio_part = task_part.rsplit("(", 1)
                task_name = name_part.strip()
                priority = prio_part.replace(")", "").strip()
            except:
                task_name = task_part
        else:
            task_name = task_part

        result.append({
            "task_name": task_name,
            "start_time": start_time,
            "end_time": end_time,
            "priority": priority
        })
    return result

async def write_schedule_to_notion(parsed_schedule):
    for item in parsed_schedule:
        props = {
            "Задача": {"title": [{"text": {"content": item["task_name"]}}]},
            "Дата": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
            "Начало": {"rich_text": [{"text": {"content": item["start_time"]}}]},
            "Окончание": {"rich_text": [{"text": {"content": item["end_time"]}}]},
            "Приоритет": {"select": {"name": item["priority"]}},
            "Статус": {"select": {"name": "Запланировано"}}
        }
        await notion_schedule_api.create_page(SCHEDULE_DATABASE_ID, props)
