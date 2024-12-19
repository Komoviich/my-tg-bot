from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random

router = Router()

# Храним состояние игры
active_games = {}

@router.message(Command("game"))
async def start_game(message: types.Message):
    user_id = message.from_user.id
    active_games[user_id] = random.randint(1, 100)
    await message.answer(
        "Игра началась! Я загадал число от 1 до 100. Попробуй угадать!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Завершить игру", callback_data="end_game")]
            ]
        )
    )

@router.message(lambda message: message.from_user.id in active_games)
async def process_guess(message: types.Message):
    user_id = message.from_user.id
    guess = message.text

    if not guess.isdigit():
        await message.answer("Пожалуйста, введите число от 1 до 100.")
        return

    guess = int(guess)
    target = active_games[user_id]

    if guess < target:
        await message.answer("Мое число больше!")
    elif guess > target:
        await message.answer("Мое число меньше!")
    else:
        del active_games[user_id]
        await message.answer(
            "Поздравляю! Ты угадал! 🎉",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Вернуться в главное меню", callback_data="main_menu")]
                ]
            )
        )

@router.callback_query(lambda c: c.data == "end_game")
async def end_game(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id in active_games:
        del active_games[user_id]
    await callback_query.message.edit_text("Игра завершена.")
    # Вызываем обработчик команды /start
    await start_command(callback_query.message)

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добро пожаловать в главное меню! Используйте кнопки ниже для выбора действия.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👋 Привет", callback_data="start")],
                [InlineKeyboardButton(text="✋ Пока", callback_data="stop")],
                [InlineKeyboardButton(text="🦊 Лиса", callback_data="fox")],
                [InlineKeyboardButton(text="🎮 Играть", callback_data="game")]
            ]
        )
    )
