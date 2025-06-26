import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from .dbfunctions import create_table, cmd_stats
from .handlers import cmd_quiz, cmd_start, answer_handler
from .api import API

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Берем Токен бота из файла, чтобы не светить его в коде
API_TOKEN = API
# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Заменил декораторов на регистрацию обработчика
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_quiz, F.text=="Начать игру")
dp.message.register(cmd_stats, F.text=="Результаты")
dp.message.register(cmd_quiz, Command("quiz"))
dp.message.register(cmd_stats, Command("stats"))
dp.callback_query.register(answer_handler, F.data.startswith("answer_"))

# Запуск процесса поллинга новых апдейтов
async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())