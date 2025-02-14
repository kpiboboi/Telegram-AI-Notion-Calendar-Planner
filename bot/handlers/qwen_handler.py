from aiogram.types import Message
from bot.qwen.qwen_client import qwen_chat
from bot.notion.notion_api import NotionAPI
from bot.config import CHAT_DATABASE_ID
from bot.utils.logger import logger
from datetime import datetime

notion_api = NotionAPI()

async def ask_command(message: Message):
    """Обрабатывает запрос пользователя к Qwen и сохраняет в Notion"""
    logger.info(f"Пользователь {message.from_user.id} вызвал /ask")
    user_input = message.text.replace("/ask", "").strip()

    if not user_input:
        logger.warning("⚠️ Пользователь отправил пустой запрос.")
        await message.answer("Введите вопрос после команды /ask")
        return

    try:
        # Загружаем историю чата только для данного пользователя
        logger.debug(f"Загружаем историю сообщений для ID {message.from_user.id}...")
        chat_history = await notion_api.query_database(
            CHAT_DATABASE_ID,
            {
                "filter": {
                    "property": "ID пользователя",
                    "number": {"equals": message.from_user.id}
                },
                "page_size": 10,
                "sorts": [{"property": "Дата", "direction": "descending"}]
            }
        )

        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        for item in reversed(chat_history.get("results", [])):
            props = item["properties"]
            if "Сообщение" in props and props["Сообщение"]["rich_text"]:
                user_text = props["Сообщение"]["rich_text"][0]["text"]["content"]
                messages.append({"role": "user", "content": user_text})

        # Добавляем текущее сообщение пользователя
        messages.append({"role": "user", "content": user_input})

        # Отправляем запрос к Qwen
        response = await qwen_chat(messages)
        logger.info(f"🤖 Ответ AI: {response}")

        # Сохраняем сообщение в Notion
        current_datetime = datetime.utcnow().isoformat()
        chat_entry = {
            "Пользователь": {"title": [{"text": {"content": message.from_user.full_name}}]},
            "ID пользователя": {"number": message.from_user.id},
            "Сообщение": {"rich_text": [{"text": {"content": user_input}}]},
            "Дата": {"date": {"start": current_datetime}}
        }
        await notion_api.create_page(CHAT_DATABASE_ID, chat_entry)
        logger.info(f"✅ Сообщение пользователя {message.from_user.id} сохранено в Notion")

        # Отправляем ответ пользователю
        await message.answer(response)

    except Exception as e:
        logger.error(f"❌ Ошибка при обработке /ask: {e}")
        await message.answer("⚠️ Ошибка при обработке запроса. Попробуйте позже.")