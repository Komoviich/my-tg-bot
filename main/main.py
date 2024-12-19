from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.handlers import router as main_router
from handlers.game_handler import router as game_router
from dotenv import load_dotenv
from handlers.choose_profession import router as profession_router
import asyncio
import os

load_dotenv()


API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("Токен бота не найден. Убедитесь, что файл .env содержит BOT_TOKEN=ваш_токен")

# Создание экземпляров бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрация маршрутов
dp.include_router(main_router)
dp.include_router(game_router)
dp.include_router(profession_router)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/game", description="Начать игру 'Угадай число'"),
        BotCommand(command="/start_profession", description="Начать выбор профессии"),
    ]
    await bot.set_my_commands(commands)

async def main():
    print("Бот запущен...")
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
