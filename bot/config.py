import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
CHAT_DATABASE_ID = os.getenv("NOTION_CHAT_HIS_DATABASE_ID")

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL")
QWEN_MODEL = os.getenv("QWEN_MODEL")

# print(API_TOKEN, "\n",
#       NOTION_TOKEN, "\n",
#       DATABASE_ID, "\n",
#       CHAT_DATABASE_ID, "\n",
#       DASHSCOPE_API_KEY, "\n",
#       QWEN_BASE_URL, "\n",
#       QWEN_MODEL, "\n",)
# print("DEBUG: TELEGRAM_API_TOKEN =", API_TOKEN)