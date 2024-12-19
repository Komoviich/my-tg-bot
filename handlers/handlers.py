import aiohttp
from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboard.keyboard import inline_keyboard

router = Router()

# Хендлер для команды /start
@router.message(Command(commands=["start"]))
async def start_command(message: Message):
    user_name = message.from_user.first_name or "друг"
    # Удаляем стандартную клавиатуру и отправляем inline-кнопки
    await message.answer(
        f"Привет!{user_name} Вот мои кнопки:",
        reply_markup=inline_keyboard
    )

@router.callback_query(lambda c: c.data == "choose_profession")
async def handle_choose_profession(callback_query: CallbackQuery):
    """Обработчик кнопки выбора профессии."""
    from handlers.choose_profession import start_choose
    await start_choose(callback_query.message)

# Обработчик нажатия на кнопку "Привет"
@router.callback_query(lambda c: c.data == "start")
async def handle_start(callback_query: CallbackQuery):
    user_name = callback_query.from_user.first_name or "друг"
    await callback_query.message.answer(f"Привет, {user_name}! Рад тебя видеть!")
    await callback_query.answer()

# Обработчик нажатия на кнопку "Стоп"
@router.callback_query(lambda c: c.data == "stop")
async def handle_stop(callback_query: CallbackQuery):
    user_name = callback_query.from_user.first_name or "друг"
    await callback_query.message.answer(f"До свидания, {user_name}! Буду ждать вас снова!")
    await callback_query.answer()

# Обработчик нажатия на кнопку "Лиса"
@router.callback_query(lambda c: c.data == "fox")
async def handle_fox(callback_query: CallbackQuery):
    user_name = callback_query.from_user.first_name or "друг"
    url = "https://randomfox.ca/floof/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                fox_image_url = data.get("image")
                if fox_image_url:
                    await callback_query.message.answer_photo(
                        fox_image_url, caption=f"Вот тебе случайная лиса, {user_name}! 🦊"
                    )
                else:
                    await callback_query.message.answer("Не удалось получить изображение лисы. Попробуй снова!")
            else:
                await callback_query.message.answer("Произошла ошибка при запросе. Попробуй позже!")
    await callback_query.answer()