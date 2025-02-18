from notion_client import AsyncClient
from bot.config import NOTION_TOKEN
import aiohttp

class NotionAPI:
    def __init__(self):
        self.client = AsyncClient(auth=NOTION_TOKEN)
        self.token = NOTION_TOKEN  # Добавляем token сюда!

    async def query_database(self, database_id, query_params):
        return await self.client.databases.query(**query_params, database_id=database_id)

    async def create_page(self, parent_db_id, properties):
        return await self.client.pages.create(
            parent={"database_id": parent_db_id},
            properties=properties
        )
        
    async def retrieve_page(self, page_id):
        """
        Получает данные о конкретной странице в Notion.
        """
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",  # Теперь self.token определен
            "Notion-Version": "2022-06-28"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()
