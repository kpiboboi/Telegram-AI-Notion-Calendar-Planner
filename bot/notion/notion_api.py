from notion_client import Client
from bot.config import NOTION_TOKEN

class NotionAPI:
    def __init__(self):
        self.client = Client(auth=NOTION_TOKEN)

    def query_database(self, database_id, query_params):
        return self.client.databases.query(**query_params, database_id=database_id)

    def create_page(self, parent_db_id, properties):
        return self.client.pages.create(
            parent={"database_id": parent_db_id},
            properties=properties
        )