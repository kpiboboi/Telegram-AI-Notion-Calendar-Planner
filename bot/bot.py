from aiogram import Bot, Dispatcher, executor, types

# Токен бота
API_TOKEN = '7344353011:AAEeJIHkK2vrQVin4tOTxA7rhpgC5LjMVj8'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой AI-ассистент. Чем могу помочь?")

# Обработчик текстовых сообщений
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"Ты сказал: {message.text}")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)