import logging
import sys

# Создадим основной логгер для нашего приложения
logger = logging.getLogger("telegram_ai_notion")
logger.setLevel(logging.DEBUG)  # Установи нужный уровень

# Формат сообщений
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Вывод логов в консоль
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Можно добавить вывод в файл, если хочешь
# file_handler = logging.FileHandler("bot.log", encoding="utf-8")
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# logger.info("...")   # Информационные события
# logger.debug("...")  # Подробная отладка
# logger.warning("...")# Предупреждения
# logger.error("...")  # Ошибки

# Подключаем обработчики к нашему логгеру
logger.addHandler(console_handler)