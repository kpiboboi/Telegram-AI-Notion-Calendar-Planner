from notion_client import AsyncClient
from bot.config import NOTION_TOKEN

class NotionAPI:
    def __init__(self):
        self.AsyncClient = AsyncClient(auth=NOTION_TOKEN)

    async def query_database(self, database_id, query_params):
        return await self.client.databases.query(**query_params, database_id=database_id)

    async def create_page(self, parent_db_id, properties):
        return await self.client.pages.create(
            parent={"database_id": parent_db_id},
            properties=properties
        )