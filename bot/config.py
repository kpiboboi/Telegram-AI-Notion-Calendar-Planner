import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
CHAT_DATABASE_ID = os.getenv("NOTION_CHAT_HIS_DATABASE_ID")

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")