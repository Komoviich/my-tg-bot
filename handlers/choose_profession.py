from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command

router = Router()

# Словари для хранения временного состояния
user_data = {}

# Маппинг для перевода профессий и уровней
PROFESSIONS = {
    "programmer": "Программист",
    "marketer": "Маркетолог",
    "manager": "Менеджер"
}

LEVELS = {
    "junior": "Младший",
    "middle": "Средний",
    "senior": "Старший"
}

# Кнопки для выбора профессии
profession_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Программист", callback_data="profession_programmer")],
    [InlineKeyboardButton(text="Маркетолог", callback_data="profession_marketer")],
    [InlineKeyboardButton(text="Менеджер", callback_data="profession_manager")]
])

# Кнопки для выбора уровня
level_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Младший", callback_data="level_junior")],
    [InlineKeyboardButton(text="Средний", callback_data="level_middle")],
    [InlineKeyboardButton(text="Старший", callback_data="level_senior")]
])

@router.message(Command("start_profession"))
async def start_choose(message: types.Message):
    """Начало выбора профессии."""
    await message.answer("Выберите свою профессию:", reply_markup=profession_buttons)

@router.callback_query(lambda c: c.data.startswith("profession_"))
async def choose_profession(callback_query: CallbackQuery):
    """Обработка выбора профессии."""
    profession_key = callback_query.data.split("_")[1]
    profession = PROFESSIONS[profession_key]
    user_data[callback_query.from_user.id] = {"profession": profession}
    await callback_query.message.edit_text(
        f"Вы выбрали профессию: {profession}\nТеперь выберите уровень:",
        reply_markup=level_buttons
    )

@router.callback_query(lambda c: c.data.startswith("level_"))
async def choose_level(callback_query: CallbackQuery):
    """Обработка выбора уровня."""
    level_key = callback_query.data.split("_")[1]
    level = LEVELS[level_key]
    user_id = callback_query.from_user.id

    if user_id in user_data and "profession" in user_data[user_id]:
        profession = user_data[user_id]["profession"]
        user_data[user_id]["level"] = level

        back_to_menu_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Вернуться в меню", callback_data="main_menu")]
            ]
        )

        await callback_query.message.edit_text(
            f"Вы выбрали профессию: {profession}\n"
            f"Вы выбрали уровень: {level}\n"
            f"Поздравляем с завершением выбора!",
            reply_markup = back_to_menu_button
        )
    else:
        await callback_query.message.edit_text(
            "Ошибка: Пожалуйста, начните с выбора профессии."
        )

@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback_query: CallbackQuery):
    """Возврат в главное меню."""
    main_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👋 Привет", callback_data="start")],
            [InlineKeyboardButton(text="✋ Пока", callback_data="stop")],
            [InlineKeyboardButton(text="🦊 Лиса", callback_data="fox")],
            [InlineKeyboardButton(text="🎮 Играть", callback_data="start_game")],
            [InlineKeyboardButton(text="💼 Выбор профессии", callback_data="choose_profession")]
        ]
    )
    await callback_query.message.edit_text(
        "Вы вернулись в главное меню. Выберите действие:",
        reply_markup=main_menu_keyboard
    )