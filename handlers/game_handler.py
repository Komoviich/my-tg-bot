from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from game.guess_number import GuessNumberGame

router = Router()

# Хранилище игр для пользователей
active_games = {}

@router.message(Command(commands=["game"]))
async def start_game_command(message: Message):
    user_id = message.from_user.id
    if user_id in active_games:
        await message.answer("Вы уже играете! Попробуйте угадать число.")
    else:
        active_games[user_id] = GuessNumberGame()
        await message.answer(
            "Я загадал число от 1 до 100. Попробуй угадать!"
        )

@router.callback_query(lambda c: c.data == "game")
async def start_game_button(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id in active_games:
        await callback_query.message.answer("Вы уже играете! Попробуйте угадать число.")
    else:
        active_games[user_id] = GuessNumberGame()
        await callback_query.message.answer(
            "Я загадал число от 1 до 100. Попробуй угадать!"
        )
    await callback_query.answer()

@router.message(lambda message: message.from_user.id in active_games)
async def handle_guess(message: Message):
    user_id = message.from_user.id
    guess = message.text
    if not guess.isdigit():
        await message.answer("Введите целое число от 1 до 100.")
        return

    guess = int(guess)
    game = active_games[user_id]
    result = game.make_guess(guess)

    if result == "win":
        await message.answer(f"Поздравляю! Вы угадали число {game.number}!")
        del active_games[user_id]
    elif result == "low":
        await message.answer("Загаданное число больше.")
    elif result == "high":
        await message.answer("Загаданное число меньше.")
