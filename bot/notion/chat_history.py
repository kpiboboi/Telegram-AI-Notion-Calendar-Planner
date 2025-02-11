from datetime import datetime
from bot.notion.notion_client import NotionAPI
from bot.config import CHAT_DATABASE_ID

notion_api = NotionAPI()

def save_message_to_notion(user_id, role, text):
    properties = {
        "User": {"title": [{"text": {"content": str(user_id)}}]},
        "Role": {"select": {"name": role}},
        "Message": {"rich_text": [{"text": {"content": text}}]},
        "Timestamp": {"date": {"start": datetime.now().isoformat()}}
    }
    notion_api.create_page(CHAT_DATABASE_ID, properties)

def get_last_messages_from_notion(user_id, limit=10):
    query_params = {
        "filter": {
            "property": "User",
            "title": {"equals": str(user_id)}
        },
        "sorts": [
            {"property": "Timestamp", "direction": "descending"}
        ],
        "page_size": limit
    }
    response = notion_api.query_database(CHAT_DATABASE_ID, query_params)
    records = response["results"][::-1]  # Перевернуть в хронологическом порядке

    messages = []
    for row in records:
        role = row["properties"]["Role"]["select"]["name"]
        content = row["properties"]["Message"]["rich_text"][0]["text"]["content"]
        messages.append({"role": role, "content": content})
    return messages