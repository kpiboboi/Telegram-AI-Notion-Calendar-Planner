import asyncio
import json
from bot.notion.notion_api import NotionAPI
from bot.config import DATABASE_ID

notion_tasks_api = NotionAPI()

async def test_load_tasks():
    """
    Тест: загружает задачи из Notion и проверяет rollup.
    """
    print("\n--- 🗂️ Тест загрузки задач из Notion ---\n")

    filter_obj = {
        "filter": {
            "or": [
                {"property": "Holat", "select": {"equals": "Boshlanmadi"}},
                {"property": "Holat", "select": {"equals": "Jarayonda"}}
            ]
        }
    }

    response = await notion_tasks_api.query_database(DATABASE_ID, filter_obj)

    for item in response["results"]:
        task_id = item["id"]
        props = item["properties"]

        name = props["Ishlar"].get("title", [{}])[0].get("text", {}).get("content", "Без названия")
        status = props.get("Holat", {}).get("select", {}).get("name", "Неизвестно")

        # 🟢 1. Проверяем, есть ли связь с Planner
        planner_relation = props.get("Planner", {}).get("relation", [])
        if not planner_relation:
            print(f"⚠️ {name}: нет связи с Planner, rollup не работает")
            continue

        # 🟢 2. Получаем данные из Planner
        planner_id = planner_relation[0]["id"]
        planner_data = await notion_tasks_api.client.pages.retrieve(planner_id)

        # 🟢 3. Получаем приоритет и дедлайн
        planner_props = planner_data.get("properties", {})

        priority = planner_props.get("Prioritet", {}).get("select", {}).get("name", "Нет данных")
        deadline = planner_props.get("Deadline", {}).get("date", {}).get("start", "Нет данных")

        print(f"📝 {name} | Статус: {status} | Приоритет: {priority} | Дедлайн: {deadline}")

asyncio.run(test_load_tasks())