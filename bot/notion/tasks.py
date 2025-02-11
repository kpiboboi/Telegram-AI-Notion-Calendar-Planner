from bot.notion.notion_api import NotionAPI
from bot.config import DATABASE_ID

from bot.utils.logger import logger

notion_api = NotionAPI()

def get_tasks():
    logger.debug("Получаем задачи из Notion...")
    try:
        query_params = {
            "sorts": [
                {"property": "Prioritet", "direction": "ascending"}
            ]
        }
    
        results = notion_api.query_database(DATABASE_ID, query_params)
        tasks = []

        for item in results["results"]:
            props = item["properties"]
            task_name = props["Ishlar"]["title"][0]["text"]["content"]
            status = props["Holat"]["select"]["name"] if props["Holat"]["select"] else "N/A"
            tasks.append((task_name, status))
        
        logger.debug(f"Получено {len(tasks)} задач.")

        return tasks
    
    except Exception as e:
        logger.error(f"Ошибка при запросе к Notion: {e}")
        return []

def add_task(task_name):
    properties = {
        "Ishlar": {"title": [{"text": {"content": task_name}}]},
        "Holat": {"select": {"name": "Boshlanmadi"}}
    }
    notion_api.create_page(DATABASE_ID, properties) 