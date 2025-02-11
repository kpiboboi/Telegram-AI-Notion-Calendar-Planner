# Telegram-AI-Notion-Calendar-Planner

*Пользователь* -> Telegram -> **GPT анализирует** -> Бот отправляет команду -> **Notion обновляется**
                                        **↑**                                                                                        ↓
                             *Обратная связь через напоминания и предложения по изменениям*

`pip instal aiogram`

`pip install notion-client`

`pip install requests`

Telegram-AI-Notion-Calendar-Planner/
├─ bot/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ config.py
│  ├─ notion/
│  │  ├─ __init__.py
│  │  ├─ notion_service.py
│  │  └─ tasks.py
│  ├─ handlers/
│  │  ├─ __init__.py
│  │  ├─ tasks_handler.py
│  │  ├─ help_handler.py
│  │  └─ qwen_handler.py
│  ├─ qwen/
│  │  ├─ __init__.py
│  │  └─ qwen_client.py
│  └─ utils/
│      ├─ __init__.py
│      └─ logger.py
└─ .env
