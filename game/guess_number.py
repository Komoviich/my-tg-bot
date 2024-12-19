from aiogram import types
import random

class GuessNumberGame:
    def __init__(self):
        self.number = random.randint(1, 100)

    def make_guess(self, guess: int) -> str:
        if guess == self.number:
            return "win"
        elif guess < self.number:
            return "low"
        else:
            return "high"
