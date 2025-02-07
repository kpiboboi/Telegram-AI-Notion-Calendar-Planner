from notion_client import Client

# Токен и база данных
NOTION_TOKEN = "ntn_z9322824063OAb2X09FATRWu7HbeNSJj2Jo5qWTp6nd7mn"
DATABASE_ID = "19322baf017f80e9b0b6cce05db1db90"

# Инициализация клиента
notion = Client(auth=NOTION_TOKEN)

def get_simple_tasks():
    try:
        response = notion.databases.query(
            **{
                "database_id": DATABASE_ID
            }
        )
        # Проверим базовую информацию о задачах
        for task in response['results']:
            task_name = task['properties']['Ishlar']['title'][0]['text']['content']
            print(f"Задача: {task_name}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    get_simple_tasks()