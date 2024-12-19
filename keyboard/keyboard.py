from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Определение inline-кнопок
inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👋 Привет", callback_data="start")],
    [InlineKeyboardButton(text="✋ Пока", callback_data="stop")],
    [InlineKeyboardButton(text="🦊 Лиса", callback_data="fox")],
    [InlineKeyboardButton(text="🎮 Играть", callback_data="start_game")],
    [InlineKeyboardButton(text="💼 Выбор профессии", callback_data="choose_profession")]
])
